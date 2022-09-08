import re
import pandas 

from .models import *
from .serializers import *
from project.services import *
from project.constaints import *
from notifications.tasks import *

from django.db.models import Count

from rest_framework import generics,permissions,filters,response,status
from django_filters.rest_framework import DjangoFilterBackend





class CreateEvent(generics.CreateAPIView,):
    '''class that allows you to create a new event'''
    serializer_class = CreateUpdateEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()

    def perform_create(self, serializer):
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
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request,pk: int):
        try:
            event = self.queryset.get(id = pk)
            if event.author.id == request.user.id:
                event.delete()
                return response.Response(EVENT_DELETE_SUCCESS,status=status.HTTP_200_OK)
            return response.Response(NO_PERMISSIONS_ERROR,status=status.HTTP_403_FORBIDDEN)
        except:
            return response.Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)


class UpdateEvent(generics.GenericAPIView):
    serializer_class = CreateUpdateEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()

    def put(self, request,pk: int):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        try:
            event = self.queryset.filter(id = pk)
            if event[0].author.id == request.user.id:
                send_notification_to_subscribe_event_user(event = event[0],notification_text='event_updated')
                event.update(**serializer.validated_data)
                return response.Response(EVENT_UPDATE_SUCCESS,status=status.HTTP_200_OK)
            return response.Response(NO_PERMISSIONS_ERROR,status=status.HTTP_403_FORBIDDEN)
        except:
            return response.Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_404_NOT_FOUND)
  
class EventList(generics.ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class =  EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter,)
    pagination_class = CustomPagination
    search_fields = ('id','name','small_disc','price','place','date_and_time','amount_members')
    ordering_fields = ('id',)
    filterset_fields = ('type', 'need_ball','gender','status','duration')
    queryset = Event.objects.all().order_by('-id')

class DeleteEvents(generics.GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class = DeleteIventsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        for i in range(len(serializer.validated_data["event_id"])):
            v_data = serializer.validated_data["event_id"] 
            self.queryset.filter(id = serializer.validated_data["event_id"][i]).delete()
        return response.Response({
            "deleted": v_data
        })

class JoinToEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

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
                return response.Response(JOIN_EVENT_SUCCES,status=status.HTTP_200_OK)
            return response.Response(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,status=status.HTTP_400_BAD_REQUEST)
        return response.Response(ALREADY_IN_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class FanJoinToEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if not user.current_views_rooms.filter(id=serializer.data['event_id']).exists():
            user.current_views_rooms.add(event)
            return response.Response(JOIN_EVENT_SUCCES,status=status.HTTP_200_OK)
        return response.Response(ALREADY_IN_FANS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)

class FanLeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_views_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_views_rooms.remove(event)
            return response.Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return response.Response(NO_IN_FANS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class LeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_rooms.filter(id = serializer.data['event_id']).exists():
            user.current_rooms.remove(event)
            return response.Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return response.Response(NO_IN_MEMBERS_LIST_ERROR,status=status.HTTP_400_BAD_REQUEST)


class UserEvents(generics.ListAPIView):
    serializer_class =  EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
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

class UserPlannedEvents(generics.ListAPIView):
    serializer_class =  EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    pagination_class = CustomPagination
    queryset = Event.objects.filter(status = 'Planned')

    def list(self, request,pk):
        pagination_class =  CustomPagination
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
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return response.Response(NO_SUCH_USER_ERROR,status=status.HTTP_400_BAD_REQUEST)