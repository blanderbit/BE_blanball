from .models import Event,RequestToParticipation
from project.celery import app
from notifications.tasks import send_notification_to_subscribe_event_user
from project.constaints import EVENT_TIME_NOTIFICATION_MESSAGE_TYPE

from django.utils import timezone



@app.task
def check_event_start_time():
    for event in Event.objects.all():
        if event.date_and_time - timezone.now() == timezone.timedelta(minutes=1440):
            send_notification_to_subscribe_event_user(event = event,notification_text = '24 hours',
            message_type=EVENT_TIME_NOTIFICATION_MESSAGE_TYPE)
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=120):
            send_notification_to_subscribe_event_user(event = event,notification_text = '1 hour',
            message_type=EVENT_TIME_NOTIFICATION_MESSAGE_TYPE)
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes=10):
            send_notification_to_subscribe_event_user(event = event,notification_text = '10 minutes',
            message_type=EVENT_TIME_NOTIFICATION_MESSAGE_TYPE)
        elif event.date_and_time == timezone.now():
            event.status = 'Active'
            event.save()
        elif ((event.date_and_time - timezone.now()) / timezone.timedelta(days=1))*1440 + event.duration <= 0:
            event.status = 'Finished'
            event.save()


@app.task
def delete_uproved_requests_to_participation():
    for request in RequestToParticipation.objects.all():
        if request.event.status == 'Finished':
            request.delete()