from typing import Any
from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from events.constants.notification_types import (
    NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE,
)
from events.models import (
    RequestToParticipation,
)
from notifications.tasks import send_to_user


@receiver(post_save, sender=RequestToParticipation)
def after_send_request_to_participation(
    sender: RequestToParticipation, instance: RequestToParticipation, **kwargs: Any
) -> None:
    if instance.status == instance.Status.WAITING:
        send_to_user(
            user=instance.recipient,
            message_type=NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE,
            data={
                "recipient": {
                    "id": instance.recipient.id,
                    "name": instance.recipient.profile.name,
                    "last_name": instance.recipient.profile.last_name,
                },
                "request": {"id": instance.id},
                "sender": {
                    "id": instance.sender.id,
                    "name": instance.sender.profile.name,
                    "last_name": instance.sender.profile.last_name,
                },
                "event": {
                    "id": instance.event.id,
                    "name": instance.event.name,
                },
            },
        )
