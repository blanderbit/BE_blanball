from rest_framework import serializers,status
from .models import Notification
from events.models import Event
from project.constaints import EVENT_NOT_FOUND_ERROR


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
