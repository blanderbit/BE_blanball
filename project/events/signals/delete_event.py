from django.db.models.signals import pre_delete
from django.dispatch import receiver
from events.constants.notification_types import (
    EVENT_DELETE_NOTIFICATION_TYPE,
)
from events.models import Event
from events.services import (
    send_notification_to_subscribe_event_user,
)


@receiver(pre_delete, sender=Event)
def delete_event(sender: Event, instance: Event, **kwargs) -> None:
    send_notification_to_subscribe_event_user(
        event=instance, message_type=EVENT_DELETE_NOTIFICATION_TYPE
    )
