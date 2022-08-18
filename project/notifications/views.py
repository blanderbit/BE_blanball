from .serializers import *
from .models import *
from rest_framework import generics


class CreateNotification(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer