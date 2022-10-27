from typing import Any, Type, final

from events.models import (
    Event,
    RequestToParticipation,
    InviteToEvent,
)
from events.serializers import (
    BulkAcceptOrDeclineRequestToParticipationSerializer,
    RequestToParticipationSerializer,
    PopularIventsListSerializer,
    JoinOrRemoveRoomSerializer,
    DeleteIventsSerializer,
    EventListSerializer,
    UpdateEventSerializer,
    EventSerializer,
    InviteUserToEventSerializer,
    CreateEventSerializer,
    InvitesToEventListSerializer,
    RemoveUserFromEventSerializer,
)
from events.services import (
    validate_user_before_join_to_event,
    filter_event_by_user_planned_events_time,
    bulk_accpet_or_decline_requests_to_participation,
    bulk_delete_events,
    send_notification_to_event_author,
    send_notification_to_subscribe_event_user,
    event_create,
    only_author,
    bulk_accept_or_decline_invites_to_events,
    remove_user_from_event,
    not_in_black_list,
)
from events.filters import (
    EventDateTimeRangeFilter, 
)

from notifications.tasks import *
from authentication.filters import RankedFuzzySearchFilter

from django.db.models import Count
from django.db.models.query import QuerySet
from django.db.models import Q

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.mixins import (
    RetrieveModelMixin,
)
from rest_framework.serializers import (
    Serializer,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

from events.constant.response_success import (
    SENT_INVATION_SUCCESS, JOIN_TO_EVENT_SUCCESS, APPLICATION_FOR_PARTICIPATION_SUCCESS,
    EVENT_UPDATE_SUCCESS, DISCONNECT_FROM_EVENT_SUCCESS,
    USER_REMOVED_FROM_EVENT_SUCCESS,
)
from events.constant.response_error import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, EVENT_NOT_FOUND_ERROR, NO_IN_EVENT_FANS_LIST_ERROR,
    NO_IN_EVENT_MEMBERS_LIST_ERROR, EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,
)
from events.constant.notification_types import (
    EVENT_UPDATE_NOTIFICATION_TYPE, LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_TYPE, 
)

from authentication.constant.errors import (
    NO_SUCH_USER_ERROR
)
from project.exceptions import _404

class CreateEvent(GenericAPIView):
    '''class that allows you to create a new event'''
    serializer_class: Type[Serializer] = CreateEventSerializer
    queryset: QuerySet[Event] = Event.get_all()
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, Any] = event_create(data = serializer.validated_data, request_user = request.user)
        return Response(data, status = HTTP_201_CREATED)


class InviteUserToEvent(GenericAPIView):
    serializer_class: Type[Serializer] = InviteUserToEventSerializer
    
    def post(self,request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        invite_user: User = User.objects.get(id = serializer.validated_data['user_id'])
        event: Event = Event.objects.get(id = serializer.validated_data['event_id'])
        InviteToEvent.objects.send_invite(request_user = request.user, invite_user = invite_user, 
            event = event)
        return Response(SENT_INVATION_SUCCESS, status = HTTP_200_OK)


class GetEvent(RetrieveModelMixin, GenericAPIView):
    '''a class that allows you to get an event'''
    serializer_class: Type[Serializer] = EventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    @not_in_black_list
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateEvent(GenericAPIView):
    serializer_class: Type[Serializer] = UpdateEventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    @only_author(Event)
    def put(self, request: Request, pk: int) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        event: Event = self.queryset.filter(id = pk).select_related('author').prefetch_related('current_users', 'current_fans')
        send_notification_to_subscribe_event_user(event = event[0], message_type = EVENT_UPDATE_NOTIFICATION_TYPE)
        event.update(**serializer.validated_data)
        return Response(EVENT_UPDATE_SUCCESS, status = HTTP_200_OK)
  
class DeleteEvents(GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class: Type[Serializer] = DeleteIventsSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, list[int]] = bulk_delete_events(
            data = serializer.validated_data['ids'], queryset = self.queryset, user = request.user)
        return Response(data, status = HTTP_200_OK)


class JoinToEvent(GenericAPIView):
    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user: User = request.user
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        validate_user_before_join_to_event(user = user, event = event)
        if not event.privacy:
            user.current_rooms.add(event)
            send_notification_to_event_author(event = event, request_user = request.user)
            return Response(JOIN_TO_EVENT_SUCCESS, status = HTTP_200_OK)
        RequestToParticipation.objects.create(recipient = event.author, sender = user, event = event)
        return Response(APPLICATION_FOR_PARTICIPATION_SUCCESS, status = HTTP_200_OK)


class FanJoinToEvent(GenericAPIView):
    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request:Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user: User = request.user
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        if event.author.id == request.user.id:
            raise ValidationError(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, HTTP_400_BAD_REQUEST)
        if not user.current_views_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_views_rooms.add(event)
            return Response(JOIN_TO_EVENT_SUCCESS, status = HTTP_200_OK)
        return Response(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, status = HTTP_400_BAD_REQUEST)

class FanLeaveFromEvent(GenericAPIView):
    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user: User = request.user
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_views_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_views_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status = HTTP_200_OK)
        return Response(NO_IN_EVENT_FANS_LIST_ERROR, status = HTTP_400_BAD_REQUEST)


class LeaveFromEvent(GenericAPIView):
    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user: User = request.user
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_rooms.remove(event)
            send_to_user(user = event.author, message_type = LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_TYPE, 
            data = {
                'recipient': {
                    'id': event.author.id,
                    'name': event.author.profile.name,
                    'last_name': event.author.profile.last_name
                },
                'event': {
                    'id': event.id,
                    'name': event.name, #+++++++++++++++++++++++++++++
                },
                'sender': {
                    'id': user.id,
                    'name': user.profile.name,
                    'last_name': user.profile.last_name
                }
            })
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status = HTTP_200_OK)
        return Response(NO_IN_EVENT_MEMBERS_LIST_ERROR, status = HTTP_400_BAD_REQUEST)


class RemoveUserFromEvent(GenericAPIView):
    serializer_class: Type[Serializer] = RemoveUserFromEventSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        user: User = User.objects.get(id = serializer.data['user_id'])
        if request.user.id != event.author.id:
            raise PermissionDenied()
        remove_user_from_event(user = user, event = event, 
            reason = serializer.validated_data['reason'])
        return Response(USER_REMOVED_FROM_EVENT_SUCCESS, status = HTTP_200_OK)

class EventList(ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class: Type[Serializer] = EventListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter, ]
    search_fields: list[str] = ['id', 'name', 'price', 'place', 'date_and_time', 'amount_members']
    ordering_fields: list[str] = ['id', ]
    filterset_class = EventDateTimeRangeFilter
    queryset: QuerySet[Event] = Event.get_all()

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(~Q(black_list__in = [self.request.user.id]))
    

class EventsRelevantList(ListAPIView):
    filter_backends = [RankedFuzzySearchFilter]
    serializer_class: Type[Serializer] = EventListSerializer
    queryset: QuerySet[Event] = Event.get_all()
    search_fields: list[str] = ['name']

    def get_queryset(self) -> QuerySet[Event]:
        return EventList.get_queryset(self)


class UserEventsRelevantList(EventsRelevantList):

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(author_id = self.request.user.id)

class InvitesToEventList(ListAPIView):
    serializer_class: Type[Serializer] = InvitesToEventListSerializer
    queryset: QuerySet[InviteToEvent] = InviteToEvent.get_all().filter(status = InviteToEvent.Status.WAITING)

    def get_queryset(self) -> QuerySet[InviteToEvent]:
        return self.queryset.filter(recipient = self.request.user)

class BulkAcceptOrDeclineInvitesToEvent(GenericAPIView):
    serializer_class: Type[Serializer] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[Event] = InviteToEvent.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, int] = bulk_accept_or_decline_invites_to_events(
            data = serializer.validated_data, request_user = request.user)
        return Response(data, status = HTTP_200_OK)

class UserEvents(EventList):

    def get_queryset(self) -> QuerySet[Event]:
        return EventList.get_queryset(self).filter(author_id = self.request.user.id) 

class UserParticipantEvents(UserEvents):

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(current_users__in = [self.request.user.id])

class PopularEvents(UserEvents):
    serializer_class: Type[Serializer] = PopularIventsListSerializer
    queryset: QuerySet[Event] = Event.get_all().filter(status = 'Planned')

    def get_queryset(self) -> QuerySet[Event]:
        return EventList.get_queryset(self).annotate(count = Count('current_users')).order_by('-count')[:10]

class UserPlannedEvents(UserEvents):
    serializer_class: Type[Serializer] = PopularIventsListSerializer
    queryset: QuerySet[Event] = Event.get_all().filter(status = 'Planned')

    def list(self, request: Request, pk: int) -> Response:
        try:
            serializer = self.serializer_class(
                filter_event_by_user_planned_events_time(pk = pk, queryset = self.queryset.all()), many = True)
            return Response(serializer.data, status = HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR, status = HTTP_400_BAD_REQUEST)


class RequestToParticipationsList(ListAPIView):
    serializer_class: Type[Serializer] = RequestToParticipationSerializer
    queryset: QuerySet[RequestToParticipation] = RequestToParticipation.get_all()
    
    def list(self, request: Request, pk: int) -> Response:
        try:
            event: Event =  Event.objects.get(id = pk)
            queryset = self.queryset.filter(event = event)
            serializer = self.serializer_class(queryset, many = True)
            return Response(serializer.data, status = HTTP_200_OK)
        except Event.DoesNotExist:
            raise _404(object = RequestToParticipation)

    
class BulkAcceptOrDeclineRequestToParticipation(GenericAPIView):
    serializer_class: Type[Serializer] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[RequestToParticipation] = RequestToParticipation.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, list[int]] = bulk_accpet_or_decline_requests_to_participation(
            data = serializer.validated_data, request_user = request.user)
        return Response(data, status = HTTP_200_OK)