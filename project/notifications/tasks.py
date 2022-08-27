from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from events.models import Event
from notifications.models import Notification
from channels.layers import get_channel_layer
from project.celery import app
from django.utils import timezone

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



def event_start_time_notifications(event,text):
    for user in event.current_users.all():
        send_to_user(user=user,notification_text=text)


@app.task
def check_event_start_time():
    for event in Event.objects.all():
        if event.date_and_time - timezone.now() == timezone.timedelta(minutes=1440):
            event_start_time_notifications(event = event,text = '24 hours')
            print('24 hours')
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=120):
            event_start_time_notifications(event = event,text = '2 hour')
            print('2 hours')
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=60):
            print('1 hours')
            event_start_time_notifications(event = event,text = '1 hour')

