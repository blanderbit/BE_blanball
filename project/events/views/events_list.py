# ==============================================================================
# events_list.py file which includes all controllers responsible for working
# with events lists, search, filtering, sorting, selection and relevant search
# ==============================================================================

from typing import Any, Type, final

from authentication.filters import (
    RankedFuzzySearchFilter,
)
from authentication.models import User
from config.exceptions import _404
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from events.filters import (
    EVENTS_LIST_DISTANCE_ORDERING_FIELD,
    EVENTS_LIST_ORDERING_FIELDS,
    EVENTS_LIST_SEARCH_FIELDS,
    EVENTS_RELEVANT_LIST_SEARCH_FIELDS,
    EventDateTimeRangeFilter,
)
from events.models import Event
from events.openapi import (
    events_list_query_params,
    events_relevant_list_query_params,
)
from events.serializers import (
    EventListSerializer,
    PopularEventsListSerializer,
)
from events.services import (
    add_dist_filter_to_view,
    filter_event_by_user_planned_events_time,
    skip_objects_from_response_by_id,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from rest_framework_gis.filters import (
    DistanceToPointOrderingFilter,
)


@method_decorator(
    swagger_auto_schema(manual_parameters=events_list_query_params),
    name="get",
)
class EventsList(ListAPIView):
    """
    List of events

    This endpoint allows the user to receive,
    filter and sort the complete list of site events.
    """

    serializer_class: Type[Serializer] = EventListSerializer
    search_fields = EVENTS_LIST_SEARCH_FIELDS
    ordering_fields = EVENTS_LIST_ORDERING_FIELDS
    filterset_class = EventDateTimeRangeFilter
    queryset: QuerySet[Event] = Event.get_all()
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        DistanceToPointOrderingFilter,
    ]
    distance_ordering_filter_field: str = EVENTS_LIST_DISTANCE_ORDERING_FIELD
    distance_filter_convert_meters: bool = True

    @skip_objects_from_response_by_id
    @add_dist_filter_to_view
    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(~Q(black_list__in=[self.request.user.id]))


@method_decorator(
    swagger_auto_schema(manual_parameters=events_relevant_list_query_params),
    name="get",
)
class EventsRelevantList(ListAPIView):
    """
    Relevant events search

    This endpoint allows you to get the 5
    most relevant events for the entered search term.
    Endpoint supports searching with typos and grammatical
    errors, as well as searching by the content of letters
    """

    filter_backends = [RankedFuzzySearchFilter]
    serializer_class: Type[Serializer] = EventListSerializer
    queryset: QuerySet[Event] = Event.get_all()
    search_fields: list[str] = EVENTS_RELEVANT_LIST_SEARCH_FIELDS

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Event]:
        return EventsList.get_queryset(self)


class UserEventsRelevantList(EventsRelevantList):
    """
    Relevant my events search

    This endpoint allows you to get the 5
    most relevant events for the entered search term.
    Endpoint supports searching with typos and grammatical
    errors, as well as searching by the content of letters
    """

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(author_id=self.request.user.id)


class UserEventsList(EventsList):
    """
    List of my events

    This endpoint allows the user to get, filter,
    sort the list of events on which he is the author
    """

    def get_queryset(self) -> QuerySet[Event]:
        return EventsList.get_queryset(self).filter(author_id=self.request.user.id)


class UserParticipantEventsList(EventsList):
    """
    List of the user participation history

    This endpoint allows the user to get information
    about his history of participation in events.
    """

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(current_users__in=[self.request.user.id])


class PopularEventsList(ListAPIView):
    """
    List of the most popular events

    This endpoint allows the user to get the first 10
    scheduled events. Sorting occurs by the number of
    active users at the event
    """

    serializer_class: Type[Serializer] = PopularEventsListSerializer
    queryset: QuerySet[Event] = Event.get_all().filter(status=Event.Status.PLANNED)

    def get_queryset(self) -> QuerySet[Event]:
        return (
            EventsList.get_queryset(self)
            .annotate(count=Count("current_users"))
            .order_by("-count")[:10]
        )


class UserPlannedEventsList(EventsList):
    """
    List of user planned events

    This endpoint makes it possible to get
    a list of other user's scheduled events.
    Scheduled events are displayed depending
    on the value in the user profile in the
    get_planned_events field.
    If the user has a value of 1m, then the
    records will be displayed one month ahead.
    """

    serializer_class: Type[Serializer] = PopularEventsListSerializer
    queryset: QuerySet[Event] = Event.get_all().filter(status=Event.Status.PLANNED)

    @skip_objects_from_response_by_id
    def list(self, request: Request, pk: int) -> Response:
        try:
            serializer = self.serializer_class(
                filter_event_by_user_planned_events_time(
                    pk=pk, queryset=self.queryset.all()
                ),
                many=True,
            )
            return Response(serializer.data, status=HTTP_200_OK)
        except User.DoesNotExist:
            raise _404(object=User)