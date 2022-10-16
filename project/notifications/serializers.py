from typing import Union

from notifications.models import Notification

from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model: Notification = Notification
        fields: Union[str, list[str]] = '__all__'


class UserNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model: Notification = Notification
        fields: Union[str, list[str]] = [
            'notification_text',
            'time_created',
        ]


class ReadOrDeleteNotificationsSerializer(serializers.Serializer):
    ids: list[int] = serializers.ListField(child = serializers.IntegerField(min_value = 0))

    class Meta:
        fields: Union[str, list[str]] = [
            'ids', 
        ]

class ChangeMaintenanceSerializer(serializers.Serializer):
    isMaintenance: bool = serializers.BooleanField() 

    class Meta:
        fields: Union[str, list[str]] = [
            'isMaintenance', 
        ]