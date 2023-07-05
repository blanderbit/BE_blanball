from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from events.constants.notification_types import (
    EVENT_HAS_BEEN_ENDEN_NOTIFICATION_TYPE,
)
from events.models import (
    Event,
)
from events.utils import (
    send_message_to_all_event_users as send_message_to_all_event_users
)


@receiver(post_save, sender=Event)
def send_message_the_end_of_event(sender: Event, instance: Event, **kwargs) -> None:
    if instance.status == instance.Status.FINISHED:
        send_message_to_all_event_users(
            event=instance,
            message_type=EVENT_HAS_BEEN_ENDEN_NOTIFICATION_TYPE,
            data={
                "event": {
                    "id": instance.id,
                    "name": instance.name,
                }
            },
        )
