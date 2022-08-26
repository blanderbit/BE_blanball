from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from events.models import Event
from notifications.models import Notification
from channels.layers import get_channel_layer
from project.celery import app


def send_to_user(user,notification_text):
    channel_layer = get_channel_layer()
    Notification.objects.create(user=user,text=f'{notification_text}')
    async_to_sync(channel_layer.group_send)(
        user.group_name,
        {
            'type': 'kafka.message',
            'message': notification_text
        }
    )

# @app.task
# @database_sync_to_async
# def notify_event(notification_text,room_group_name):
#     event = Event.objects.get(name = room_group_name )
#     for user in event.current_users.all():
#         Notification.objects.create(user=user,text=user.profile.name + notification_text)
#         send_to_user(user=user,notification_text=notification_text)
