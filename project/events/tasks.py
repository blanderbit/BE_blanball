from .models import Event
from project.celery import app
from notifications.tasks import send_notification_to_subscribe_event_user

from django.utils import timezone



@app.task
def check_event_start_time():
    for event in Event.objects.all():
        # print(event.date_and_time + event.duration)
        if event.date_and_time - timezone.now() == timezone.timedelta(minutes=1440):
            send_notification_to_subscribe_event_user(event = event,notification_text = '24 hours')
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=120):
            send_notification_to_subscribe_event_user(event = event,notification_text = '1 hour')
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=10):
            send_notification_to_subscribe_event_user(event = event,notification_text = '10 minutes')
        elif event.date_and_time == timezone.now():
            event.status = 'Active'
            event.save()
        elif ((event.date_and_time - timezone.now()) / timezone.timedelta(days=1))*1440 + event.duration <= 0:
            event.status = 'Finished'
            event.save()