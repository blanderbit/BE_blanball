import re
import pandas

from .models import *
from .serializers import *
from project.services import *
from project.constaints import *
from notifications.tasks import *
from authentication.fuzzy_filter import RankedFuzzySearchFilter

from django.db.models import Count
from django.db.models.query import QuerySet


from rest_framework import generics,filters,status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class CreateEvent(generics.GenericAPIView):
    '''class that allows you to create a new event'''
    serializer_class = CreateEventSerializer
    queryset = Event.objects.all()

    def post(self,request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        for user in serializer.validated_data['current_users']:
            if user.email == request.user.email:
                return Response(SENT_INVATION_ERROR,status=status.HTTP_400_BAD_REQUEST)
            send_to_user(user = user,notification_text=INVITE_USER_NOTIFICATION.format(
            user_name=request.user.profile.name,event_name = serializer.validated_data['name']),
            message_type=INVITE_USER_TO_EVENT_MESSAGE_TYPE)
        self.perform_create(serializer=serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

    def perform_create(self,serializer) -> None:
        serializer.validated_data.pop('current_users')
        try:
            contact_number:str = serializer.validated_data['contact_number']
        except:
            contact_number:str = User.objects.get(id = self.request.user.id).phone
        serializer.save(author=self.request.user,date_and_time = 
        pandas.to_datetime(serializer.validated_data['date_and_time'].isoformat()).round('1min').to_pydatetime(),
        contact_number=contact_number)        

class InviteUserToEvent(generics.GenericAPIView):
    serializer_class = InviteUserToEventSerializer
    
    def post(self,request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            invite_user:User = User.objects.get(id = serializer.validated_data['user_id'])
            if invite_user.id == request.user.id:
                return Response(SENT_INVATION_ERROR,status=status.HTTP_400_BAD_REQUEST)
            event:Event = Event.objects.get(id = serializer.validated_data['event_id'])
            if not invite_user.current_rooms.filter(id=event.id).exists():
                send_to_user(user = invite_user,notification_text=
                INVITE_USER_NOTIFICATION.format(user_name=request.user.profile.name,event_name=event.name),
                message_type=INVITE_USER_TO_EVENT_MESSAGE_TYPE)
                return Response(SENT_INVATION_SUCCESS,status=status.HTTP_200_OK)
            return Response(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_404_NOT_FOUND)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)



class GetDeleteEvent(generics.RetrieveAPIView):
    '''a class that allows you to get, update, delete an event'''
    serializer_class =  EventSerializer
    queryset = Event.objects.all()
    
    def delete(self, request,pk:int) -> Response:
        try:
            event:Event = self.queryset.get(id = pk)
            if event.author.id == request.user.id:
                event.delete()
                return Response(EVENT_DELETED_SUCCESS,status=status.HTTP_200_OK)
            return Response(NO_PERMISSIONS_ERROR,status=status.HTTP_403_FORBIDDEN)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)


class UpdateEvent(generics.GenericAPIView):
    serializer_class = UpdateEventSerializer
    queryset = Event.objects.all()

    def put(self, request,pk: int) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        try:
            event:list[Event] = self.queryset.filter(id = pk)
            if event[0].author.id == request.user.id:
                send_notification_to_subscribe_event_user(event = event[0],
                notification_text='event_updated',message_type=EVENT_UPDATE_MESSAGE_TYPE)
                event.update(**serializer.validated_data)
                return Response(EVENT_UPDATE_SUCCESS,status=status.HTTP_200_OK)
            return Response(NO_PERMISSIONS_ERROR,status=status.HTTP_403_FORBIDDEN)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)
  
class EventList(generics.ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class =  EventListSerializer
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter,)
    filterset_class = EventDateTimeRangeFilter
    pagination_class = CustomPagination
    search_fields = ('id','name','small_disc','price','place','date_and_time','amount_members')
    ordering_fields = ('id',)
    filterset_fields = ('type', 'need_ball','gender','status','duration')
    queryset = Event.objects.all().order_by('-id')

class DeleteEvents(generics.GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class = DeleteIventsSerializer
    queryset = Event.objects.all()

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deleted:list = [] 
        not_deleted:list= []
        for event_id in serializer.validated_data['events']:
            event:Event =  self.queryset.filter(id = event_id)
            if event:
                event = self.queryset.get(id = event_id)
                if event.user == request.user:
                    event.delete()
                    deleted.append(event_id)
                else:
                    not_deleted.append(event_id)
            else:
                not_deleted.append(event_id)
        return Response({"delete success": deleted, "delete error":  not_deleted},status=status.HTTP_200_OK)


class JoinToEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:User = request.user
        event:Event = Event.objects.get(id = serializer.data['event_id'])
        if not user.current_rooms.filter(id=event.id).exists():
            if not user.current_views_rooms.filter(id=event.id).exists():
                if event.author_id != user.id:
                    if event.amount_members != event.count_current_users:
                        if not event.privacy:
                            user.current_rooms.add(event)
                            send_notification_to_event_author(event)
                            return Response(JOIN_TO_EVENT_SUCCESS,status=status.HTTP_200_OK)
                        else:
                            if not RequestToParticipation.objects.filter(user=user,event=event.id,event_author=event.author):
                                send_to_user(user=event.author,notification_text=
                                NEW_REQUEST_TO_PARTICIPATION.format(author_name=event.author.profile.name,event_id=event.id),
                                message_type=NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE)
                                RequestToParticipation.objects.create(user=user,event_id=event.id,event_author=event.author)
                                return Response(APPLICATION_FOR_PARTICIPATION_SUCCESS,status=status.HTTP_200_OK)
                            return Response(ALREADY_SENT_REQUEST_TO_PARTICIPATE,status=status.HTTP_400_BAD_REQUEST)
                return Response(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,status=status.HTTP_400_BAD_REQUEST)
            return Response(ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR,status=status.HTTP_400_BAD_REQUEST)
        return Response(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class FanJoinToEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:User = request.user
        event:Event = Event.objects.get(id = serializer.data['event_id'])
        if not user.current_views_rooms.filter(id=serializer.data['event_id']).exists():
            user.current_views_rooms.add(event)
            return Response(JOIN_TO_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return Response(ALREADY_IN_EVENT_FANS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)

class FanLeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:User = request.user
        event:Event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_views_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_views_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return Response(NO_IN_EVENT_FANS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class LeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user:User = request.user
        event:Event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return Response(NO_IN_EVENT_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)

class EventsRelevantList(generics.ListAPIView):
    filter_backends = (RankedFuzzySearchFilter,)
    serializer_class = EventListSerializer
    queryset = Event.objects.all()
    search_fields = ('name',)

class UserEventsRelevantList(EventsRelevantList):
    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(author_id = self.request.user.id) 

class UserEvents(generics.ListAPIView):
    serializer_class =  EventListSerializer
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    pagination_class = CustomPagination
    search_fields = ['id','name','small_disc','price','place','date_and_time','amount_members']
    filterset_fields = ['type']
    queryset = Event.objects.all() 

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(author_id = self.request.user.id) 

class PopularIvents(UserEvents):
    serializer_class = PopularIventsListSerializer
    queryset = Event.objects.filter(status = 'Planned')

    def get_queryset(self) -> QuerySet:
        return self.queryset.annotate(count = Count('current_users')).order_by('-count')[:10]

class UserPlannedEvents(UserEvents):
    serializer_class = PopularIventsListSerializer
    queryset = Event.objects.filter(status = 'Planned')

    def list(self, request,pk:int) -> Response:
        try:
            user:User =  User.objects.get(id=pk)
            num = re.findall(r'\d{1,10}', user.get_planned_events)[0]
            string = re.findall(r'\D', user.get_planned_events)[0]
            if string == 'd':
                num = int(num[0])
            elif string == 'm':  
                num = int(num[0])*30 + int(num[0])//2
            elif string == 'y':
                num = int(num[0])*365
            finish_date = timezone.now() + timezone.timedelta(days=int(num))
            queryset = self.queryset.filter(author_id = user.id,date_and_time__range=[timezone.now(),finish_date])
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_400_BAD_REQUEST)


    
class RequestToParticipationsList(generics.ListAPIView):
    serializer_class = RequestToParticipationSerializer
    queryset = RequestToParticipation.objects.all().order_by('-id')
    

    def list(self,request,pk:int) -> Response:
        try:
            event:Event =  Event.objects.get(id=pk)
            queryset = self.queryset.filter(event=event)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)

    

class BulkAcceptOrDeclineRequestToParticipation(generics.GenericAPIView):
    serializer_class = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset = RequestToParticipation.objects.all()

    def post(self,request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        success:list = []
        not_success:list = []
        for request_id in serializer.validated_data['requests']:
            request_to_p = self.queryset.filter(id = request_id)
            if request_to_p:
                request_to_p = self.queryset.get(id = request_id)
                if request_to_p.event_author.id == request.user.id:
                    if serializer.validated_data['type'] == True:
                        send_to_user(user=request_to_p.user,notification_text=RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION.format(
                            user_name=request_to_p.user.profile.name,event_id=request_to_p.event.id,response_type='прийнято'),
                            message_type=RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                        success.append(request_id)
                        request_to_p.user.current_rooms.add(request_to_p.event)
                        request_to_p.delete()
                    else:
                        send_to_user(user=request_to_p.user,notification_text=RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION.format(
                            user_name=request_to_p.user.profile.name,event_id=request_to_p.event.id,response_type='відхилено'),
                            message_type=RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                        success.append(request_id)
                        request_to_p.delete()
                else:
                    not_success.append(request_id)
            else:
                not_success.append(request_id)
            return Response({"success": success, "error":  not_success},status=status.HTTP_200_OK)