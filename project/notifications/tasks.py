from datetime import datetime
from typing import Any, Union

from notifications.models import Notification
from authentication.models import (
    User,
)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_user(user: User, message_type: str, data: dict[str, Union[str, int, datetime, bool]] = None) -> None:
    channel_layer = get_channel_layer()
    notification = Notification.objects.create(user = user, message_type = message_type, data = data)
    async_to_sync(channel_layer.group_send)(
        user.group_name,
        {
            'type': 'kafka.message',
            'message_type': message_type, 
            'notification_id': notification.id,
            'data': data
        }
    )

def send_to_scedular(user: User, data: dict[str, Any]) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        user.group_name,
        {
            'type': 'kafka.message',
            'message_type': 'scedular', 
            'data': data
        }
    )