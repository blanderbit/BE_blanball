import re
import pandas

from .models import *
from .serializers import *
from project.services import *
from project.constaints import *
from notifications.tasks import *

from django.db.models import Count

from rest_framework import generics,filters,status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend



class CreateEvent(generics.GenericAPIView):
    '''class that allows you to create a new event'''
    serializer_class = CreateEventSerializer
    queryset = Event.objects.all()

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        for user in serializer.validated_data['current_users']:
                send_to_user(user = user,notification_text=INVITE_USER_NOTIFICATION.format(
                user_name=request.user.profile.name,event_id=1))
        self.perform_create(serializer=serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

    def perform_create(self,serializer):
        serializer.validated_data.pop('current_users')
        try:
            contact_number = serializer.validated_data['contact_number']
        except:
            contact_number = User.objects.get(id = self.request.user.id).phone
        serializer.save(author=self.request.user,date_and_time = 
        pandas.to_datetime(serializer.validated_data['date_and_time']).round('1min'),contact_number=contact_number)        


class GetDeleteEvent(generics.RetrieveAPIView):
    '''a class that allows you to get, update, delete an event'''
    serializer_class =  EventSerializer
    queryset = Event.objects.all()
    
    def delete(self, request,pk: int):
        try:
            event = self.queryset.get(id = pk)
            if event.author.id == request.user.id:
                event.delete()
                return Response(EVENT_DELETED_SUCCESS,status=status.HTTP_200_OK)
            return Response(NO_PERMISSIONS_ERROR,status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)


class UpdateEvent(generics.GenericAPIView):
    serializer_class = UpdateEventSerializer
    queryset = Event.objects.all()

    def put(self, request,pk: int):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        try:
            event = self.queryset.filter(id = pk)
            if event[0].author.id == request.user.id:
                send_notification_to_subscribe_event_user(event = event[0],notification_text='event_updated')
                event.update(**serializer.validated_data)
                return Response(EVENT_UPDATE_SUCCESS,status=status.HTTP_200_OK)
            return Response(NO_PERMISSIONS_ERROR,status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)
  
class EventList(generics.ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class =  EventListSerializer
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter,)
    pagination_class = CustomPagination
    search_fields = ('id','name','small_disc','price','place','date_and_time','amount_members')
    ordering_fields = ('id',)
    filterset_fields = ('type', 'need_ball','gender','status','duration')
    queryset = Event.objects.all().order_by('-id')

class DeleteEvents(generics.GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class = DeleteIventsSerializer
    queryset = Event.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deleted = [] 
        not_deleted = []
        for event in serializer.validated_data['events']:
            notify =  self.queryset.filter(id = event)
            if notify:
                notify = self.queryset.get(id = event)
                if notify.user == request.user:
                    notify.delete()
                    deleted.append(event)
                else:
                    not_deleted.append(event)
            else:
                not_deleted.append(event)
        return Response({"delete success": deleted, "delete error":  not_deleted},status=status.HTTP_200_OK)

class JoinToEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        
        if not user.current_rooms.filter(id=serializer.data['event_id']).exists():
            if event.author_id != user.id:
                if event.amount_members > event.count_current_users+1:
                    send_to_user(user = User.objects.get(id = event.author.id),notification_text= '+1 user')
                    user.current_rooms.add(event)
                elif event.amount_members == event.count_current_users+1:
                    send_to_user(user = User.objects.get(id = event.author.id),notification_text= '+1 user and all places')
                    user.current_rooms.add(event)
                return Response(JOIN_EVENT_SUCCES,status=status.HTTP_200_OK)
            return Response(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,status=status.HTTP_400_BAD_REQUEST)
        return Response(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class FanJoinToEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if not user.current_views_rooms.filter(id=serializer.data['event_id']).exists():
            user.current_views_rooms.add(event)
            return Response(JOIN_EVENT_SUCCES,status=status.HTTP_200_OK)
        return Response(ALREADY_IN_EVENT_FANS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)

class FanLeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_views_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_views_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return Response(NO_IN_EVENT_FANS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class LeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return Response(NO_IN_EVENT_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class UserEvents(generics.ListAPIView):
    serializer_class =  EventListSerializer
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    pagination_class = CustomPagination
    search_fields = ['id','name','small_disc','price','place','date_and_time','amount_members']
    filterset_fields = ['type']
    queryset = Event.objects.all() 

    def get_queryset(self):
        return self.queryset.filter(author_id = self.request.user) 

class PopularIvents(UserEvents):
    queryset = Event.objects.filter(status = 'Planned')

    def get_queryset(self):
        return self.queryset.annotate(count = Count('current_users')).order_by('-count')[:10]

class UserPlannedEvents(UserEvents):
    queryset = Event.objects.filter(status = 'Planned')

    def list(self, request,pk):
        try:
            user =  User.objects.get(id=pk)
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
        except:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_400_BAD_REQUEST)

class InviteUserToEvent(generics.GenericAPIView):
    serializer_class = InviteUserToEventSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            invite_user = User.objects.get(id = serializer.validated_data['user_id'])
            if invite_user.id == request.user.id:
                return Response(SENT_INVATION_ERROR,status=status.HTTP_400_BAD_REQUEST)
            event = Event.objects.get(id = serializer.validated_data['event_id'])
            send_to_user(user = invite_user,notification_text=INVITE_USER_NOTIFICATION.format(user_name=request.user.profile.name,event_id=event.id))
            return Response(SENT_INVATION_SUCCESS,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_404_NOT_FOUND)
        except Event.DoesNotExist:
            return Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)