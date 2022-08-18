from urllib import request
from django.shortcuts import render

from .serializers import NotificationSerializer

from .models import Notification
from rest_framework import generics,permissions,status,response,views

class UserNotificationsList(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Notification.objects.filter(user = request.user)) 
