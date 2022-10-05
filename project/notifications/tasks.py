from notifications.models import Notification
from authentication.models  import User,ActiveUser
from events.models import Event

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_to_user(user: User, notification_text: str, message_type: str) -> None:
    channel_layer = get_channel_layer()
    Notification.objects.create(user = user, notification_text = notification_text)
    if ActiveUser.objects.filter(user = user.id):
        async_to_sync(channel_layer.group_send)(
            user.group_name,
            {
                'type': 'kafka.message',
                'message': notification_text,
                'message_type': message_type, 
            }
        )


def send_notification_to_subscribe_event_user(event: Event, notification_text: str, message_type: str) -> None:
    for user in event.current_users.all():
        send_to_user(user = user, notification_text = notification_text, message_type = message_type)
    for fan in event.fans.all():
        send_to_user(user = fan, notification_text = notification_text, message_type = message_type)