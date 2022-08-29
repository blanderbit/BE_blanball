from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_text','date_time']


class ReadOrDeleteNotificationsSerializer(serializers.Serializer):
    notifications = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        fields = ['notifications']