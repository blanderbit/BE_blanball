from typing import Any, Type

from yaml import serialize

from events.models import (
    Event,
    RequestToParticipation,
    EventTemplate,
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
    TemplateCreateSerializer,
    TemplateListSerializer,
    TemplateGetSerializer,
    InvitesToEventListSerializer,
)
from events.services import (
    validate_user_before_join_to_event,
    filter_event_by_user_planned_events_time,
    bulk_accpet_or_decline_requests_to_participation,
    bulk_delete_events,
    send_notification_to_event_author,
    send_notification_to_subscribe_event_user,
    validate_get_user_planned_events,
    event_create,
    only_author,
    validate_invited_users,
    bulk_accept_or_decline_invites_to_events,
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
    RetrieveAPIView,
)
from rest_framework.serializers import (
    Serializer,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from events.constants import (
    SENT_INVATION_ERROR, INVITE_USER_TO_EVENT_MESSAGE_TYPE, INVITE_USER_NOTIFICATION, SENT_INVATION_SUCCESS,
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, EVENT_NOT_FOUND_ERROR, EVENT_DELETED_SUCCESS, EVENT_UPDATE_MESSAGE_TYPE,
    EVENT_UPDATE_SUCCESS, JOIN_TO_EVENT_SUCCESS, NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE, NEW_REQUEST_TO_PARTICIPATION, 
    APPLICATION_FOR_PARTICIPATION_SUCCESS, NO_IN_EVENT_FANS_LIST_ERROR, DISCONNECT_FROM_EVENT_SUCCESS, 
    EVENT_TEMPLATE_UPDATE_SUCCESS, EVENT_TEMPLATE_NOT_FOUND_ERROR, LEAVE_USER_FROM_THE_EVENT_NOTIFICATION, 
    NO_IN_EVENT_MEMBERS_LIST_ERROR, EVENT_UPDATE_TEXT, AUTHOR_CAN_NOT_INVITE_ERROR, EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,

)
from authentication.constants import (
    NO_SUCH_USER_ERROR, NO_PERMISSIONS_ERROR
)


class CreateEvent(GenericAPIView):
    '''class that allows you to create a new event'''
    serializer_class: Type[Serializer] = CreateEventSerializer
    queryset: QuerySet[Event] = Event.get_event_list()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        validate_invited_users(request_user = request.user, users = serializer.validated_data['current_users'])
        data: dict[str, Any] = event_create(data = serializer.validated_data, request_user = request.user)
        return Response(data, status = HTTP_201_CREATED)

class CreateEventTemplate(GenericAPIView):
    serializer_class: Type[Serializer] = TemplateCreateSerializer
    queryset: QuerySet[EventTemplate] = EventTemplate.get_event_template_list()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        EventTemplate.objects.create(author = request.user, **request.data)
        return Response(serializer.data)

class EventsTemplateList(ListAPIView):
    serializer_class: Type[Serializer] = TemplateListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter, ]
    search_fields: list[str] = ['name', 'time_created']
    ordering_fields: list[str] = ['id', ]
    queryset: QuerySet[EventTemplate] = EventTemplate.get_event_template_list()

    def get_queryset(self) -> QuerySet[EventTemplate]:
        return self.queryset.filter(author_id = self.request.user.id) 


class UpdateEventTemplate(GenericAPIView):
    serializer_class: Type[Serializer] = TemplateCreateSerializer
    queryset: QuerySet[EventTemplate] = EventTemplate.get_event_template_list()

    @only_author(EventTemplate)
    def put(self, request: Request, pk: int) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        EventTemplate.objects.filter(id = pk).update(**request.data)
        return Response(EVENT_TEMPLATE_UPDATE_SUCCESS, status = HTTP_200_OK)


class GetEventTemplate(GenericAPIView):
    serializer_class: Type[Serializer] = TemplateGetSerializer
    queryset: QuerySet[EventTemplate] = EventTemplate.get_event_template_list()

    @only_author(EventTemplate)
    def get(self, request: Request, pk: int) -> Response:
        event_template: EventTemplate = EventTemplate.objects.get(id = pk)
        serializer = self.serializer_class(event_template)
        return Response(serializer.data, status = HTTP_200_OK)

class InviteUserToEvent(GenericAPIView):
    serializer_class: Type[Serializer] = InviteUserToEventSerializer
    
    def post(self,request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        invite_user: User = User.objects.get(id = serializer.validated_data['user_id'])
        event: Event = Event.objects.get(id = serializer.validated_data['event_id'])
        if invite_user.id == request.user.id:
            return Response(SENT_INVATION_ERROR, status = HTTP_400_BAD_REQUEST)
        InviteToEvent.objects.send_invite(request_user = request.user, invite_user = invite_user, 
            event = event)
        return Response(SENT_INVATION_SUCCESS, status = HTTP_200_OK)

class GetEvent(RetrieveAPIView):
    '''a class that allows you to get an event'''
    serializer_class: Type[Serializer] =  EventSerializer
    queryset: QuerySet[Event] = Event.get_event_list()

class UpdateEvent(GenericAPIView):
    serializer_class: Type[Serializer] = UpdateEventSerializer
    queryset: QuerySet[Event] = Event.get_event_list()

    @only_author(Event)
    def put(self, request: Request, pk: int) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        event: Event = self.queryset.filter(id = pk).select_related('author').prefetch_related('current_users', 'current_fans')
        send_notification_to_subscribe_event_user(event = event[0],
        notification_text = EVENT_UPDATE_TEXT.format(event_id = event[0].id), message_type = EVENT_UPDATE_MESSAGE_TYPE)
        event.update(**serializer.validated_data)
        return Response(EVENT_UPDATE_SUCCESS, status = HTTP_200_OK)
  
class DeleteEvents(GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class: Type[Serializer] = DeleteIventsSerializer
    queryset: QuerySet[Event] = Event.get_event_list()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, list[int]] = bulk_delete_events(
            data = serializer.validated_data['ids'], queryset = self.queryset, user = request.user)
        return Response(data, status = HTTP_200_OK)

class DeleteEventTemplates(DeleteEvents):
    queryset: QuerySet[Event] = EventTemplate.get_event_template_list()

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
            send_notification_to_event_author(event = event)
            return Response(JOIN_TO_EVENT_SUCCESS, status = HTTP_200_OK)
        else:
            RequestToParticipation.objects.create(user = user, event_id = event.id, event_author = event.author)
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
            send_to_user(user = event.author, notification_text=
                LEAVE_USER_FROM_THE_EVENT_NOTIFICATION.format(author_name = event.author.profile.name, event_id = event.id),
                message_type = NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status = HTTP_200_OK)
        return Response(NO_IN_EVENT_MEMBERS_LIST_ERROR, status = HTTP_400_BAD_REQUEST)

from django.utils import timezone

class EventsRelevantList(ListAPIView):
    filter_backends = [RankedFuzzySearchFilter]
    serializer_class: Type[Serializer] = EventListSerializer
    queryset: QuerySet[Event] = Event.get_event_list()
    search_fields: list[str] = ['name']

class UserEventsSceduler(ListAPIView):
    serializer_class: Type[Serializer] = EventListSerializer
    queryset: QuerySet[Event] = Event.get_event_list()

    def get_queryset(self) -> QuerySet[Event]:
        # query = Q(current_users__in = [self.request.user.id])
        # query.add(Q(current_users__in = [self.request.user.id]))
        print(timezone.now().date().weekday())
        return self.queryset.filter(Q(author_id = self.request.user.id) | Q(current_users__in = [self.request.user.id]))

class UserEventsRelevantList(EventsRelevantList):

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(author_id = self.request.user.id)

class EventList(ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class: Type[Serializer] = EventListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter, ]
    search_fields: list[str] = ['id', 'name', 'price', 'place', 'date_and_time', 'amount_members']
    ordering_fields: list[str] = ['id', ]
    filterset_class = EventDateTimeRangeFilter
    queryset: QuerySet[Event] = Event.get_event_list()

class InvitesToEventList(ListAPIView):
    serializer_class: Type[Serializer] = InvitesToEventListSerializer
    queryset: QuerySet[Event] = InviteToEvent.get_invite_to_event_list()

class BulkAcceptOrDeclineInvitesToEvent(GenericAPIView):
    serializer_class: Type[Serializer] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[Event] = InviteToEvent.get_invite_to_event_list()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, int] = bulk_accept_or_decline_invites_to_events(
            data = serializer.validated_data, request_user = request.user)
        return Response(data, status = HTTP_200_OK)

class UserEvents(EventList):

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(author_id = self.request.user.id) 

class UserParticipantEvents(UserEvents):

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(current_users__in = [self.request.user.id])

class PopularEvents(UserEvents):
    serializer_class: Type[Serializer] = PopularIventsListSerializer
    queryset: QuerySet[Event] = Event.get_event_list().filter(status = 'Planned')

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.annotate(count = Count('current_users')).order_by('-count')[:10]

class UserPlannedEvents(UserEvents):
    serializer_class: Type[Serializer] = PopularIventsListSerializer
    queryset: QuerySet[Event] = Event.get_event_list().filter(status = 'Planned')

    def list(self, request: Request, pk: int) -> Response:
        try:
            validate_get_user_planned_events(pk = pk, request_user = request.user)
            serializer = self.serializer_class(
                filter_event_by_user_planned_events_time(pk = pk, queryset = self.queryset.all()), many = True)
            return Response(serializer.data, status = HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR, status = HTTP_400_BAD_REQUEST)


class RequestToParticipationsList(ListAPIView):
    serializer_class: Type[Serializer] = RequestToParticipationSerializer
    queryset: QuerySet[RequestToParticipation] = RequestToParticipation.get_request_to_participation_list()
    
    def list(self, request: Request, pk: int) -> Response:
        try:
            event: Event =  Event.objects.get(id = pk)
            queryset = self.queryset.filter(event = event)
            serializer = self.serializer_class(queryset, many = True)
            return Response(serializer.data, status = HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR, status = HTTP_404_NOT_FOUND)

    
class BulkAcceptOrDeclineRequestToParticipation(GenericAPIView):
    serializer_class: Type[Serializer] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[RequestToParticipation] = RequestToParticipation.get_request_to_participation_list()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        data: dict[str, list[int]] = bulk_accpet_or_decline_requests_to_participation(
            data = serializer.validated_data, user = request.user)
        return Response(data, status = HTTP_200_OK)