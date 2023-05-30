from typing import Union

from authentication.models import User
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

    def to_representation(self, instance):
        data = super().to_representation(instance)

        try:
            sender = User.objects.get(id=data["data"]["sender"]["id"])
            data["data"]["sender"]["avatar"] = sender.profile.avatar_url
            data["data"]["sender"]["is_online"] = sender.is_online
        except KeyError:
            pass
        except User.DoesNotExist:
            pass

        try:
            recipient = User.objects.get(id=data["data"]["recipient"]["id"])
            data["data"]["recipient"]["avatar"] = recipient.profile.avatar_url
        except KeyError:
            pass
        except User.DoesNotExist:
            pass

        return data


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
