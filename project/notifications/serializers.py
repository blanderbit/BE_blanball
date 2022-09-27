from notifications.models import Notification

from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'notification_text',
            'time_created',
        )


class ReadOrDeleteNotificationsSerializer(serializers.Serializer):
    notifications = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        fields = ('notifications',)

class ChangeMaintenanceSerializer(serializers.Serializer):
    isMaintenance = serializers.BooleanField() 

    class Meta:
        fields = ('isMaintenance',)