from typing import Union

from events.constants.notification_types import (
    INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
)
from events.models import (
    InviteToEvent,
    RequestToParticipation,
)
from notifications.models import Notification
from notifications.tasks import send


def send_update_message_after_response(
    *, instance: Union[InviteToEvent, RequestToParticipation], message_type: str
) -> None:
    if instance.status != instance.Status.WAITING:
        try:
            status: dict[str, bool] = {
                instance.Status.ACCEPTED: True,
                instance.Status.DECLINED: False,
            }
            notification = Notification.objects.get(
                message_type=INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
                data__invite__id=instance.id,
            )
            send(
                user=instance.recipient,
                data={
                    "type": "kafka.message",
                    "message": {
                        "message_type": message_type,
                        "notification": {
                            "id": notification.id,
                            "message_type": notification.message_type,
                            "response": status[instance.status],
                        },
                    },
                },
            )
            notification.data.update({"response": status[instance.status]})
            notification.save()

        except Notification.DoesNotExist:
            pass
