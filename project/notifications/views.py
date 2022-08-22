from urllib import request
from .serializers import *
from .models import *
from rest_framework import generics,permissions


class CreateNotification(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


class UserNotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id = self.request.user.id)