from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver
from events.constants.notification_types import (
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT,
)
from events.models import InviteToEvent
from events.utils import (
    send_update_message_after_response,
)


@receiver(post_save, sender=InviteToEvent)
def send_message_after_response_to_invite_to_event(
    sender: InviteToEvent, instance: InviteToEvent, **kwargs: Any
) -> None:
    send_update_message_after_response(
        instance=instance, message_type=UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT
    )
