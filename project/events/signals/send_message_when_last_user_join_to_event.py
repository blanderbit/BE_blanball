from typing import Any

from authentication.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from events.constants.notification_types import (
    LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
    YOU_ARE_LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
)
from events.models import Event
from notifications.tasks import send_to_user


@receiver(m2m_changed, sender=Event.current_users.through)
def send_message_when_last_user_join_to_event(
    sender: User, instance: User, **kwargs: Any
) -> None:
    action: str = kwargs.pop("action", None)
    if action == "post_add":
        event: Event = instance.current_rooms.through.objects.last().event
        if event.current_users.all().count() + 1 == event.amount_members:
            for user in list(event.current_users.all()) + [event.author]:
                if user == instance:
                    message_type: str = YOU_ARE_LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE
                else:
                    message_type: str = LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE
                send_to_user(
                    user,
                    message_type=message_type,
                    data={
                        "event": {
                            "id": event.id,
                            "name": event.name,
                        }
                    },
                )
