from typing import Any, Type, final

from authentication.filters import (
    RankedFuzzySearchFilter,
)
from config.exceptions import _404
from config.openapi import skip_param_query
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from events.constants.notification_types import (
    EVENT_UPDATE_NOTIFICATION_TYPE,
)
from events.constants.response_error import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,
    EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,
    NO_IN_EVENT_FANS_LIST_ERROR,
    NO_IN_EVENT_MEMBERS_LIST_ERROR,
)
from events.constants.response_success import (
    APPLICATION_FOR_PARTICIPATION_SUCCESS,
    DISCONNECT_FROM_EVENT_SUCCESS,
    EVENT_UPDATE_SUCCESS,
    JOIN_TO_EVENT_SUCCESS,
    SENT_INVATION_SUCCESS,
    USER_REMOVED_FROM_EVENT_SUCCESS,
)
from events.filters import (
    EventDateTimeRangeFilter,
)
from events.models import (
    Event,
    InviteToEvent,
    RequestToParticipation,
)
from events.openapi import (
    events_list_query_params,
    events_relevant_list_query_params,
)
from events.serializers import (
    BulkAcceptOrDeclineRequestToParticipationSerializer,
    CreateEventSerializer,
    DeleteEventsSerializer,
    EventListSerializer,
    EventSerializer,
    InvitesToEventListSerializer,
    InviteUserToEventSerializer,
    JoinOrRemoveRoomSerializer,
    PopularEventsListSerializer,
    RemoveUserFromEventSerializer,
    RequestToParticipationSerializer,
    UpdateEventSerializer,
)
from events.services import (
    add_dist_filter_to_view,
    bulk_accept_or_decline_invites_to_events,
    bulk_accpet_or_decline_requests_to_participation,
    bulk_delete_events,
    event_create,
    filter_event_by_user_planned_events_time,
    not_in_black_list,
    only_author,
    remove_user_from_event,
    send_message_to_event_author_after_leave_user_from_event,
    send_notification_to_event_author,
    send_notification_to_subscribe_event_user,
    skip_objects_from_response_by_id,
    validate_user_before_join_to_event,
)
from notifications.tasks import *
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.mixins import (
    RetrieveModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework_gis.filters import (
    DistanceToPointOrderingFilter,
)


class CreateEvent(GenericAPIView):
    """
    Event create

    This endpoint allows the user to create an event.
    The user can also specify the ID of other users in
    the current_users field to send them invitations.

    privacy true - means that it will not be possible
    to simply connect to the event, everything will go
    through the rejection or acceptance of applications
    by the author of the event.

    privacy false - means that the event has open access
    and anyone can connect to it.

    gender field options: Man, Wooman
    type field options: Football, Futsal
    forms field options: Shirt-Front, T-Shirt, Any
    duration field options: 10, 20, 30, 40, 50, 60, 70,
    80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180",
    """

    serializer_class: Type[Serializer] = CreateEventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, Any] = event_create(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_201_CREATED)


class InviteUserToEvent(GenericAPIView):
    """
    Invite user to event

    This endpoint allows the author of the event
    and the user who is a participant in the event
    to send invitations to participate in this event
    """

    serializer_class: Type[Serializer] = InviteUserToEventSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_user: User = User.get_all().get(id=serializer.validated_data["user_id"])
        event: Event = Event.get_all().get(id=serializer.validated_data["event_id"])
        InviteToEvent.objects.send_invite(
            request_user=request.user, invite_user=invite_user, event=event
        )
        return Response(SENT_INVATION_SUCCESS, status=HTTP_200_OK)


class GetEvent(RetrieveModelMixin, GenericAPIView):
    """
    Get event

    This endpoint allows the user, with the exception
    of those blacklisted for this event,
    get detailed information about any event.
    """

    serializer_class: Type[Serializer] = EventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    @not_in_black_list
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateEvent(GenericAPIView):
    """
    Update event

    This endpoint allows the event author
    to change any data on the event
    """

    serializer_class: Type[Serializer] = UpdateEventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    @only_author(Event)
    def put(self, request: Request, pk: int) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        event: Event = self.queryset.filter(id=pk)
        send_notification_to_subscribe_event_user(
            event=event[0], message_type=EVENT_UPDATE_NOTIFICATION_TYPE
        )
        event.update(**serializer.validated_data)
        return Response(EVENT_UPDATE_SUCCESS, status=HTTP_200_OK)


class DeleteEvents(GenericAPIView):
    """
    Delete event

    This endpoint allows the user to delete
    their events.If the user deletes the event,
    it can no longer be restored.
    """

    serializer_class: Type[Serializer] = DeleteEventsSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_delete_events(
            data=serializer.validated_data["ids"],
            queryset=self.queryset,
            user=request.user,
        )
        return Response(data, status=HTTP_200_OK)


class JoinToEvent(GenericAPIView):
    """
    Join the event as a member

    This endpoint allows a user who is not the
    author of this event and is not  already on the
    participants or viewers list to enter the event as a participant.
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.get_all().get(id=serializer.data["event_id"])
        validate_user_before_join_to_event(user=user, event=event)
        if not event.privacy:
            user.current_rooms.add(event)
            send_notification_to_event_author(event=event, request_user=request.user)
            return Response(JOIN_TO_EVENT_SUCCESS, status=HTTP_200_OK)
        RequestToParticipation.objects.create(
            recipient=event.author, sender=user, event=event
        )
        return Response(APPLICATION_FOR_PARTICIPATION_SUCCESS, status=HTTP_200_OK)


class FanJoinToEvent(GenericAPIView):
    """
    Join the event as a spectator

    This endpoint allows a user who is not the
    author of this event and is not  already on the
    participants or viewers list to enter the event as a viewer.
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.get_all().get(id=serializer.data["event_id"])
        if event.author.id == request.user.id:
            raise ValidationError(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, HTTP_400_BAD_REQUEST)
        if not user.current_views_rooms.filter(id=serializer.data["event_id"]).exists():
            user.current_views_rooms.add(event)
            return Response(JOIN_TO_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(
            ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, status=HTTP_400_BAD_REQUEST
        )


class FanLeaveFromEvent(GenericAPIView):
    """
    Leave the event as a spectator

    This endpoint allows the user who is
    at the event as a spectator to leave it
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.get_all().get(id=serializer.data["event_id"])
        if user.current_views_rooms.filter(id=serializer.data["event_id"]).exists():
            user.current_views_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(NO_IN_EVENT_FANS_LIST_ERROR, status=HTTP_400_BAD_REQUEST)


class LeaveFromEvent(GenericAPIView):
    """
    Leave the event as a member

    This endpoint allows the user who is
    at the event as a participant to leave it
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.get_all().get(id=serializer.data["event_id"])
        if user.current_rooms.filter(id=serializer.data["event_id"]).exists():
            user.current_rooms.remove(event)
            send_message_to_event_author_after_leave_user_from_event(
                event=event, user=user
            )
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(NO_IN_EVENT_MEMBERS_LIST_ERROR, status=HTTP_400_BAD_REQUEST)


class RemoveUserFromEvent(GenericAPIView):
    """
    Exclude a user from an event

    This endpoint allows the event author to
    remove (kick) the user from the event for
    one reason or another.
    """

    serializer_class: Type[Serializer] = RemoveUserFromEventSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        event: Event = Event.get_all().get(id=serializer.data["event_id"])
        user: User = User.get_all().get(id=serializer.data["user_id"])
        if request.user.id != event.author.id:
            raise PermissionDenied()
        remove_user_from_event(
            user=user, event=event, reason=serializer.validated_data["reason"]
        )
        return Response(USER_REMOVED_FROM_EVENT_SUCCESS, status=HTTP_200_OK)


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
    search_fields: list[str] = [
        "id",
        "name",
        "price",
        "amount_members",
    ]
    ordering_fields: list[str] = [
        "id",
    ]
    filterset_class = EventDateTimeRangeFilter
    queryset: QuerySet[Event] = Event.get_all()
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        DistanceToPointOrderingFilter,
    ]
    distance_ordering_filter_field: str = "coordinates"
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
    search_fields: list[str] = ["name"]

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


@method_decorator(
    swagger_auto_schema(manual_parameters=[skip_param_query]),
    name="get",
)
class InvitesToEventList(ListAPIView):
    """
    List of my invitations to events

    This endpoint allows the user to
    view all of his event invitations.
    """

    serializer_class: Type[Serializer] = InvitesToEventListSerializer
    queryset: QuerySet[InviteToEvent] = InviteToEvent.get_all().filter(
        status=InviteToEvent.Status.WAITING
    )

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[InviteToEvent]:
        return self.queryset.filter(recipient=self.request.user)


class BulkAcceptOrDeclineInvitesToEvent(GenericAPIView):
    """
    Accepting/declining invitations to participate in an event

    This endpoint gives the user the ability to
    accept or decline requests to participate in events.
    """

    serializer_class: Type[
        Serializer
    ] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[Event] = InviteToEvent.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, int] = bulk_accept_or_decline_invites_to_events(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_200_OK)


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


class PopularEvents(EventsList):
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


@method_decorator(swagger_auto_schema(manual_parameters=[skip_param_query]), name="get")
class RequestToParticipationsList(ListAPIView):
    """
    List of requests for participation in the event

    This endpoint allows all users to view
    applications for participation in a
    particular private event
    """

    serializer_class: Type[Serializer] = RequestToParticipationSerializer
    queryset: QuerySet[
        RequestToParticipation
    ] = RequestToParticipation.get_all().filter(
        status=RequestToParticipation.Status.WAITING
    )

    @not_in_black_list
    @skip_objects_from_response_by_id
    def list(self, request: Request, pk: int) -> Response:
        try:
            event: Event = Event.get_all().get(id=pk)
            queryset = self.queryset.filter(event=event)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Event.DoesNotExist:
            raise _404(object=Event)


class BulkAcceptOrDeclineRequestToParticipation(GenericAPIView):
    """
    Accepting/declining requests to participate in an event

    This endpoint allows the author of a private
    event to accept or reject applications for
    participation in his event.
    """

    serializer_class: Type[
        Serializer
    ] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[RequestToParticipation] = RequestToParticipation.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_accpet_or_decline_requests_to_participation(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_200_OK)
