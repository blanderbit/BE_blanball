from datetime import datetime
from typing import Any, Optional, Union

from asgiref.sync import async_to_sync
from authentication.models import User
from channels.layers import get_channel_layer
from config.celery import celery
from django.db.models import QuerySet
from django.utils import timezone
from notifications.constants.notification_types import (
    ALL_USER_NOTIFICATIONS_DELETED_NOTIFICATION_TYPE,
    ALL_USER_NOTIFICATIONS_READ_NOTIFICATION_TYPE,
)
from notifications.models import Notification


def send(
    data: dict[str, Any], user: Optional[User] = None, group_name: Optional[str] = None
) -> None:
    group_name_to_send: str = ""
    if user:
        group_name_to_send = user.group_name
    elif group_name:
        group_name_to_send = group_name
    async_to_sync(get_channel_layer().group_send)(group_name_to_send, data)


def send_to_user(
    message_type: str,
    user: User,
    data: dict[str, Union[str, int, datetime, bool]] = None,
) -> None:
    notification = Notification.objects.create(
        user=user, message_type=message_type, data=data
    )
    send(
        user=user,
        data={
            "type": "send.message",
            "message": {
                "message_type": message_type,
                "notification_id": notification.id,
                "data": data,
            },
        },
    )


def send_to_group_by_group_name(
    message_type: str,
    group_name: str,
    data: dict[str, Union[str, int, datetime, bool]] = None,
) -> None:
    send(
        group_name=group_name,
        data={
            "type": "send.message",
            "message": {
                "message_type": message_type,
                "data": data,
            },
        },
    )


def send_to_general_layer(
    message_type: str,
    data: dict[str, Union[str, int, datetime, bool]] = None,
) -> None:

    group_name_to_send: str = "general"

    send(
        group_name=group_name_to_send,
        data={
            "type": "send.message",
            "message": {
                "message_type": message_type,
                "data": data,
            },
        },
    )


@celery.task(
    ignore_result=True,
    time_limit=5,
    soft_time_limit=3,
    default_retry_delay=5,
)
def read_all_user_notifications(*, request_user_id: int) -> None:
    user_notifications: QuerySet[Notification] = Notification.get_all().filter(
        user_id=request_user_id, type=Notification.Type.UNREAD
    )
    if len(user_notifications) > 0:
        user_notifications.update(type=Notification.Type.READ)
        try:
            send(
                user=User.objects.get(id=request_user_id),
                data={
                    "type": "send.message",
                    "message": {
                        "message_type": ALL_USER_NOTIFICATIONS_READ_NOTIFICATION_TYPE,
                    },
                },
            )
        except User.DoesNotExist:
            pass


@celery.task(
    ignore_result=True,
    time_limit=5,
    soft_time_limit=3,
    default_retry_delay=5,
)
def delete_all_user_notifications(*, request_user_id: int) -> None:
    user_notifications: QuerySet[Notification] = Notification.get_all().filter(
        user_id=request_user_id
    )
    if len(user_notifications) > 0:
        user_notifications.delete()
        try:
            send(
                user=User.objects.get(id=request_user_id),
                data={
                    "type": "kafka.message",
                    "message": {
                        "message_type": ALL_USER_NOTIFICATIONS_DELETED_NOTIFICATION_TYPE,
                    },
                },
            )
        except User.DoesNotExist:
            pass


@celery.task
def delete_expire_notifications():
    Notification.objects.filter(
        time_created__lte=timezone.now() - timezone.timedelta(days=85)
    ).delete()
