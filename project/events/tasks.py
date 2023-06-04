import pandas
from config.celery import celery
from django.db.models import Q
from django.utils import timezone
from events.constants.notification_types import (
    EVENT_TIME_NOTIFICATION_TYPE,
)
from events.models import Event
from events.services import (
    send_notification_to_subscribe_event_user,
)


@celery.task
def check_event_start_time() -> None:

    rounded_current_datetime = (
        pandas.to_datetime(timezone.now().replace(second=0).isoformat())
        .round("1min", nonexistent="shift_backward")
        .to_pydatetime()
    )
    for event in Event.get_all().filter(~Q(status=Event.Status.FINISHED)):

        event_start_time_delta = event.date_and_time - rounded_current_datetime
        event_minutes_to_start = event_start_time_delta.total_seconds() / 60

        # 1 day
        if event_minutes_to_start == 24 * 60:
            send_notification_to_subscribe_event_user(
                event=event,
                message_type=EVENT_TIME_NOTIFICATION_TYPE,
                start_time=str(event.date_and_time),
                time_to_start=24 * 60,
            )
        # 2 hours
        elif event_minutes_to_start == 2 * 60:
            send_notification_to_subscribe_event_user(
                event=event,
                message_type=EVENT_TIME_NOTIFICATION_TYPE,
                start_time=str(event.date_and_time),
                time_to_start=2 * 60,
            )
        elif event_minutes_to_start == 10:
            send_notification_to_subscribe_event_user(
                event=event,
                message_type=EVENT_TIME_NOTIFICATION_TYPE,
                start_time=str(event.date_and_time),
                time_to_start=10,
            )
        elif event_minutes_to_start == 0:
            event.status = event.Status.ACTIVE
            event.save()
        elif event_minutes_to_start + event.duration == 0:
            event.status = event.Status.FINISHED
            event.save()
