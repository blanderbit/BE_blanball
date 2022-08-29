from asgiref.sync import async_to_sync
from events.models import Event
from notifications.models import Notification
from channels.layers import get_channel_layer
from project.celery import app
from authentication.models  import ActiveUser
from django.utils import timezone
from authentication.tasks import Util


def send_to_user(user,notification_text):
    channel_layer = get_channel_layer()
    Notification.objects.create(user=user,notification_text=f'{notification_text}')
    if ActiveUser.objects.filter(user = user.id):
        async_to_sync(channel_layer.group_send)(
            user.group_name,
            {
                'type': 'kafka.message',
                'message': notification_text
            }
        )
    else:
        Util.send_email.delay(data = {'email_subject': 'Your','email_body': notification_text ,
        'to_email': user.email})




def send_notification_to_subscribe_event_user(event,notification_text):
    for user in event.current_users.all():
        send_to_user(user=user,notification_text=notification_text)


@app.task
def check_event_start_time():
    for event in Event.objects.all():
        if event.date_and_time - timezone.now() == timezone.timedelta(minutes=1440):
            send_notification_to_subscribe_event_user(event = event,notification_text = '24 hours')
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=120):
            send_notification_to_subscribe_event_user(event = event,notification_text = '1 hour')
        elif event.date_and_time - timezone.now() != timezone.timedelta(minutes=10):
            send_notification_to_subscribe_event_user(event = event,notification_text = '10 minutes')

