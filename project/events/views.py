from typing import Any
import pandas

from events.models import (
    Event,
    RequestToParticipation,
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
)
from events.services import (
    validate_user_before_join_to_event,
    filter_event_by_user_planned_events_time,
    bulk_accpet_or_decline,
    bulk_delete_events,
    send_notification_to_event_author,
    send_notification_to_subscribe_event_user,
)
from events.filters import EventDateTimeRangeFilter

from project.pagination import CustomPagination
from notifications.tasks import *
from authentication.filters import RankedFuzzySearchFilter

from django.db.models import Count
from django.db.models.query import QuerySet

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
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
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from authentication.permisions import *

from events.constaints import (
    SENT_INVATION_ERROR, INVITE_USER_TO_EVENT_MESSAGE_TYPE, INVITE_USER_NOTIFICATION, SENT_INVATION_SUCCESS,
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, EVENT_NOT_FOUND_ERROR, EVENT_DELETED_SUCCESS, EVENT_UPDATE_MESSAGE_TYPE,
    EVENT_UPDATE_SUCCESS, JOIN_TO_EVENT_SUCCESS, NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE, NEW_REQUEST_TO_PARTICIPATION, 
    APPLICATION_FOR_PARTICIPATION_SUCCESS, NO_IN_EVENT_FANS_LIST_ERROR, DISCONNECT_FROM_EVENT_SUCCESS, 
    LEAVE_USER_FROM_THE_EVENT_NOTIFICATION, NO_IN_EVENT_MEMBERS_LIST_ERROR, EVENT_UPDATE_TEXT, AUTHOR_CAN_NOT_INVITE_ERROR, 

)
from authentication.constaints import (
    NO_SUCH_USER_ERROR, NO_PERMISSIONS_ERROR
)


class CreateEvent(GenericAPIView):
    '''class that allows you to create a new event'''
    serializer_class = CreateEventSerializer
    queryset = Event.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        for user in serializer.validated_data['current_users']:
            if user.email == request.user.email:
                return Response(SENT_INVATION_ERROR, status = HTTP_400_BAD_REQUEST)
            send_to_user(user = user, notification_text = INVITE_USER_NOTIFICATION.format(
            user_name = request.user.profile.name, event_name = serializer.validated_data['name']),
            message_type = INVITE_USER_TO_EVENT_MESSAGE_TYPE)
        self.perform_create(serializer = serializer)
        return Response(serializer.data, status = HTTP_201_CREATED)
        

    def perform_create(self, serializer: CreateEventSerializer) -> None:
        serializer.validated_data.pop('current_users')
        try:
            contact_number: str = serializer.validated_data['contact_number']
        except:
            contact_number: str = User.objects.get(id = self.request.user.id).phone
        serializer.save(author = self.request.user, date_and_time = 
        pandas.to_datetime(serializer.validated_data['date_and_time'].isoformat()).round('1min').to_pydatetime(),
        contact_number = contact_number)        

class InviteUserToEvent(GenericAPIView):
    serializer_class = InviteUserToEventSerializer
    
    def post(self,request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        invite_user: User = User.objects.get(id = serializer.validated_data['user_id'])
        event: Event = Event.objects.get(id = serializer.validated_data['event_id'])
        if invite_user.id == request.user.id:
            return Response(SENT_INVATION_ERROR, status = HTTP_400_BAD_REQUEST)
        send_to_user(user = invite_user,notification_text=
        INVITE_USER_NOTIFICATION.format(user_name = request.user.profile.name, event_name = event.id),
        message_type = INVITE_USER_TO_EVENT_MESSAGE_TYPE)
        return Response(SENT_INVATION_SUCCESS, status = HTTP_200_OK)

class GetDeleteEvent(RetrieveAPIView):
    '''a class that allows you to get, update, delete an event'''
    serializer_class =  EventSerializer
    queryset = Event.objects.all()
    
    def delete(self, request: Request, pk: int) -> Response:
        try:
            event: Event = self.queryset.get(id = pk)
            if event.author.id == request.user.id:
                event.delete()
                return Response(EVENT_DELETED_SUCCESS, status = HTTP_200_OK)
            return Response(NO_PERMISSIONS_ERROR, status = HTTP_403_FORBIDDEN)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR, status = HTTP_404_NOT_FOUND)


class UpdateEvent(GenericAPIView):
    serializer_class = UpdateEventSerializer
    queryset = Event.objects.all()

    def put(self, request: Request, pk: int) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        event: Event = self.queryset.filter(id = pk).select_related('author').prefetch_related('current_users', 'fans')
        try:
            if event[0].author.id == request.user.id:
                send_notification_to_subscribe_event_user(event = event[0],
                notification_text = EVENT_UPDATE_TEXT.format(event_id = event[0].id), message_type = EVENT_UPDATE_MESSAGE_TYPE)
                event.update(**serializer.validated_data)
                return Response(EVENT_UPDATE_SUCCESS, status = HTTP_200_OK)
            return Response(NO_PERMISSIONS_ERROR, status = HTTP_403_FORBIDDEN)
        except IndexError:
            return Response(EVENT_NOT_FOUND_ERROR, status = HTTP_404_NOT_FOUND)
  

class EventList(ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class =  EventListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, )
    filterset_class = EventDateTimeRangeFilter
    pagination_class = CustomPagination
    search_fields = ('id', 'name', 'small_disc', 'price', 'place', 'date_and_time', 'amount_members')
    ordering_fields = ('id', )
    filterset_fields = ('type', 'need_ball', 'gender', 'status', 'duration')
    queryset = Event.objects.all().select_related('author').prefetch_related('current_users','fans').order_by('-id')


class DeleteEvents(GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class = DeleteIventsSerializer
    queryset = Event.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(bulk_delete_events(
            serializer = serializer, queryset = self.queryset, user = request.user), status = HTTP_200_OK)


class JoinToEvent(GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user: User = request.user
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        validate_user_before_join_to_event(user = user, event = event)
        if not event.privacy:
            user.current_rooms.add(event)
            send_notification_to_event_author(event)
            return Response(JOIN_TO_EVENT_SUCCESS, status = HTTP_200_OK)
        else:
            send_to_user(user = event.author, notification_text=
            NEW_REQUEST_TO_PARTICIPATION.format(author_name = event.author.profile.name, event_id = event.id),
                message_type = NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE)
            RequestToParticipation.objects.create(user = user, event_id = event.id, event_author = event.author)
            return Response(APPLICATION_FOR_PARTICIPATION_SUCCESS, status = HTTP_200_OK)


class FanJoinToEvent(GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request:Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user: User = request.user
        event: Event = Event.objects.get(id = serializer.data['event_id'])
        if not user.current_views_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_views_rooms.add(event)
            return Response(JOIN_TO_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, status=HTTP_400_BAD_REQUEST)

class FanLeaveFromEvent(GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

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
    serializer_class = JoinOrRemoveRoomSerializer

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

class EventsRelevantList(ListAPIView):
    filter_backends = (RankedFuzzySearchFilter, )
    serializer_class = EventListSerializer
    queryset = Event.objects.all()
    search_fields = ('name', )

class UserEventsRelevantList(EventsRelevantList):

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(author_id = self.request.user.id)

class UserEvents(ListAPIView):
    serializer_class =  EventListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    pagination_class = CustomPagination
    search_fields = ['id', 'name', 'small_disc', 'price', 'place', 'date_and_time', 'amount_members']
    filterset_fields = ('type', )
    queryset = Event.objects.all()

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.filter(author_id = self.request.user.id) 

class PopularIvents(UserEvents):
    serializer_class = PopularIventsListSerializer
    queryset = Event.objects.filter(status = 'Planned')

    def get_queryset(self) -> QuerySet[Event]:
        return self.queryset.annotate(count = Count('current_users')).order_by('-count')[:10]

class UserPlannedEvents(UserEvents):
    serializer_class = PopularIventsListSerializer
    queryset = Event.objects.filter(status = 'Planned')

    def list(self, request: Request, pk: int) -> Response:
        try:
            serializer = self.serializer_class(
                filter_event_by_user_planned_events_time(pk = pk, queryset = self.queryset.all()), many = True)
            serializer = self.serializer_class(serializer.data, many=True)
            return Response(serializer.data, status = HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR, status = HTTP_400_BAD_REQUEST)

class RequestToParticipationsList(ListAPIView):
    serializer_class = RequestToParticipationSerializer
    queryset = RequestToParticipation.objects.all().order_by('-id')
    
    def list(self, request: Request, pk: int) -> Response:
        try:
            event: Event =  Event.objects.get(id = pk)
            queryset = self.queryset.filter(event = event)
            serializer = self.serializer_class(queryset, many = True)
            return Response(serializer.data, status = HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR, status = HTTP_404_NOT_FOUND)

    
class BulkAcceptOrDeclineRequestToParticipation(GenericAPIView):
    serializer_class = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset = RequestToParticipation.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(bulk_accpet_or_decline(
            serializer = serializer, user = request.user), status = HTTP_200_OK)