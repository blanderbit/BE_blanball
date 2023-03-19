from typing import Union

from notifications.models import Notification
from rest_framework.serializers import (
    BooleanField,
    IntegerField,
    ModelSerializer,
    Serializer,
)


class NotificationSerializer(ModelSerializer):
    class Meta:
        model: Notification = Notification
        fields: Union[str, list[str]] = "__all__"


class UserNotificationSerializer(ModelSerializer):
    class Meta:
        model: Notification = Notification
        fields: Union[str, list[str]] = [
            "id",
            "type",
            "time_created",
        ]


class UserNotificationsCount(Serializer):
    all_notifications_count: int = IntegerField(min_value=0)
    not_read_notifications_count: int = IntegerField(min_value=0)

    class Meta:
        fields: Union[str, list[str]] = [
            "all_notifications_count",
            "not_read_notifications_count",
        ]


class ChangeMaintenanceSerializer(Serializer):
    isMaintenance: bool = BooleanField()

    class Meta:
        fields: Union[str, list[str]] = [
            "isMaintenance",
        ]


class GetNotificationsIdsSerializer(Serializer):

    count: bool = IntegerField()

    class Meta:
        fields: Union[str, list[str]] = [
            "count",
        ]