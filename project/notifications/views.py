from urllib import request
from .serializers import *
from .models import *
from rest_framework import generics,permissions
from project.services import CustomPagination


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
