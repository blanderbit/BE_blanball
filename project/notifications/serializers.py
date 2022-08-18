from rest_framework import serializers
from .models import *


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields =  '__all__'
        ordering = ['-created_at']