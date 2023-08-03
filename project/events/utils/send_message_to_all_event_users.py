from typing import Any

from events.models import Event
from notifications.tasks import send_to_user


def send_message_to_all_event_users(
    *, event: Event, message_type: str, data: dict[str, Any]
) -> None:
    for user in list(event.current_users.all()):
        send_to_user(user, message_type=message_type, data=data)
