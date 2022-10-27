from datetime import datetime
from typing import Union

from notifications.models import Notification
from authentication.models import (
    User,
)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from notifications.constant.notification_types import (
    CHANGE_MAINTENANCE_NOTIFICATION_TYPE
)


def send_to_user(user: User, message_type: str, data: dict[str, Union[str, int, datetime, bool]] = None) -> None:
    if message_type != CHANGE_MAINTENANCE_NOTIFICATION_TYPE:
        notification = Notification.objects.create(user = user, message_type = message_type, data = data)
    async_to_sync(get_channel_layer().group_send)(
        user.group_name,
        {
            'type': 'kafka.message',
            'message_type': message_type, 
            'notification_id': notification.id,
            'data': data
        }
    )