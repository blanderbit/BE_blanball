from events.models import (
    Event,
    RequestToParticipation,
)
from config.celery import app
from events.services import send_notification_to_subscribe_event_user
from events.constant.notification_types import (
    EVENT_TIME_NOTIFICATION_TYPE,
)

from django.utils import timezone

@app.task
def check_event_start_time() -> None:
    for event in Event.get_all():
        if event.date_and_time - timezone.now() == timezone.timedelta(minutes = 1440):
            send_notification_to_subscribe_event_user(event = event, 
                message_type = EVENT_TIME_NOTIFICATION_TYPE,
                start_time = str(event.date_and_time),
                time_to_start = 1440)
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes = 120):
            send_notification_to_subscribe_event_user(event = event, 
                message_type = EVENT_TIME_NOTIFICATION_TYPE,
                start_time = str(event.date_and_time),
                time_to_start = 120)
        elif event.date_and_time - timezone.now() == timezone.timedelta(minutes = 10):
            send_notification_to_subscribe_event_user(event = event, 
                message_type = EVENT_TIME_NOTIFICATION_TYPE,
                start_time = str(event.date_and_time),
                time_to_start = 10)
        elif event.date_and_time == timezone.now():
            event.status = event.Status.ACTIVE
            event.save()
        elif ((event.date_and_time - timezone.now()) / timezone.timedelta(days = 1)) * 1440 + event.duration <= 0:
            event.status = event.Status.FINISHED
            event.save()

@app.task
def delete_requests_to_participation() -> None:
    for request in RequestToParticipation.get_all():
        if request.event.status == request.event.Status.FINISHED:
            request.delete()