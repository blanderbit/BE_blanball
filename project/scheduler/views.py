from typing import Type

from django.db.models import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from events.models import Event
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from scheduler.openapi import (
    scheduled_events_list_query_params,
)
from scheduler.serializers import (
    ListOfUserScheduledEventsOnSpecificDaySerializer,
    UserScheduledEventsSerializer,
)
from scheduler.services import (
    get_user_scheduled_events_data,
    get_user_scheduled_events_on_specific_day,
)
from utils import (
    paginate_by_offset,
    skip_objects_from_response_by_id,
)


class UserScheduledEvents(GenericAPIView):
    """
    User scheduled events

    This endpoint allows the user to
    get the number of events scheduled by
    the user for the date range
    """

    serializer_class: Type[Serializer] = UserScheduledEventsSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        scheduled_events_data = get_user_scheduled_events_data(
            serializer.validated_data, self.queryset
        )

        return Response(scheduled_events_data, status=HTTP_200_OK)


@paginate_by_offset
@method_decorator(
    swagger_auto_schema(
        manual_parameters=scheduled_events_list_query_params,
    ),
    name="get",
)
class ListOfUserScheduledEventsOnSpecificDay(ListAPIView):
    """
    List of user scheduled events on specific day

    This endpoint allows the user to
    get the list of events scheduled on specific day
    """

    serializer_class: Type[
        Serializer
    ] = ListOfUserScheduledEventsOnSpecificDaySerializer
    queryset: QuerySet[Event] = Event.get_all()

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Event]:
        return get_user_scheduled_events_on_specific_day(self.request, self.queryset)
