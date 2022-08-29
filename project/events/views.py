from rest_framework import generics,permissions,filters,response,status
from .models import *
from .serializers import *
from project.services import *
from django_filters.rest_framework import DjangoFilterBackend
from project.constaints import *
from notifications.tasks import send_notification_to_subscribe_event_user,send_to_user

class CreateEvent(generics.CreateAPIView,):
    '''class that allows you to create a new event'''
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()
        
class GetPutDeleteEvent(GetPutDeleteAPIView):
    '''a class that allows you to get, update, delete an event'''
    serializer_class =  EventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]
        
    def put(self, request,pk: int):
        obj = self.queryset.filter(id = pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        if obj:
            if obj[0].author.id == request.user.id:
                obj[0].save()
                send_notification_to_subscribe_event_user(event = obj[0],notification_text='event_updated')
                return response.Response(EVENT_UPDATE_SUCCESS,status=status.HTTP_200_OK)
            return response.Response(NO_PERMISSIONS_ERROR,status=status.HTTP_400_BAD_REQUEST)
        return response.Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk: int):
        obj = Event.objects.filter(id = pk)
        if obj:
            if obj[0].author.id == request.user.id:
                send_notification_to_subscribe_event_user(event = obj[0],notification_text='event_deleted')
                obj[0].delete()
                return response.Response(EVENT_DELETE_SUCCESS,status=status.HTTP_200_OK)
            return response.Response(NO_PERMISSIONS_ERROR,status=status.HTTP_400_BAD_REQUEST)
        return response.Response(EVENT_NOT_FOUND_ERROR,status=status.HTTP_400_BAD_REQUEST)


  
class EventList(generics.ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class =  EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    pagination_class = CustomPagination
    search_fields = ['id','name','small_disc','price','place','date_and_time','amount_members']
    filterset_fields = ['type', 'need_ball','gender']
    queryset = Event.objects.all().order_by('-id')

class DeleteEvents(generics.GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class = DeleteIventsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        for i in range(len(serializer.validated_data["dele"])):
            v_data = serializer.validated_data["dele"] 
            self.queryset.filter(id = serializer.validated_data["dele"][i]).delete()
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
            if event.amount_members > len(event.current_users.all())+1:
                send_to_user(user = User.objects.get(id = event.author.id),notification_text= '+1 user')
                user.current_rooms.add(event)
            elif event.amount_members == len(event.current_users.all())+1:
                send_to_user(user = User.objects.get(id = event.author.id),notification_text= '+1 user and all places')
                user.current_rooms.add(event)
            else:
                return response.Response(NO_EVENT_PLACE_ERROR)
            return response.Response(JOIN_EVENT_SUCCES,status=status.HTTP_200_OK)
        return response.Response(ALREADY_IN_MEMBER_LIST_ERROR)


class LeaveFromEvent(generics.GenericAPIView):
    serializer_class = JoinOrRemoveRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        if user.current_rooms.filter(id=serializer.data['event_id']).exists():
            user.current_rooms.remove(event)
            return response.Response(DISCONNECT_FROM_EVENT_SUCCESS,status=status.HTTP_200_OK)
        return response.Response(NO_IN_MEMBER_LIST_ERROR)


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