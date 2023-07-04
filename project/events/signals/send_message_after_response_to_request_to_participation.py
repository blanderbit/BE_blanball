from typing import Any
from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from events.constants.notification_types import (
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_REQUEST_TO_PARTICIPATION,
)
from events.models import (
    RequestToParticipation,
)
from events.utils import (
    send_update_message_after_response 
)

@receiver(post_save, sender=RequestToParticipation)
def send_message_after_response_to_request_to_participation(
    sender: RequestToParticipation, instance: RequestToParticipation, **kwargs: Any
) -> None:
    send_update_message_after_response(
        instance=instance,
        message_type=UPDATE_MESSAGE_ACCEPT_OR_DECLINE_REQUEST_TO_PARTICIPATION,
    )
