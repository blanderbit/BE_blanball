from .serializers import *
from .models import *
from rest_framework import generics,permissions,response
from project.services import CustomPagination
from project.constaints import *

class CreateNotification(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    queryset = Notification.objects.all()


class UserNotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Notification.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id = self.request.user.id)


class JoinEvent(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JoinOrRemoveRoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        event = Event.objects.get(id = serializer.data['event_id'])
        user.current_rooms.add()
        return response.Response(JOIN_EVENT_SUCCES) 