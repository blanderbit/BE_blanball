from django.db.models.signals import (
    post_save,
    pre_delete,
)
from django.dispatch import receiver

from notifications.models import Notification
from notifications.tasks import send

from notifications.constant.notification_types import (
    NOTIFICATION_DELETE_NOTIFICATION_TYPE,
)


@receiver(pre_delete, sender = Notification)
def send_update_message_after_delete_notification(sender: Notification, instance: Notification, **kwargs) -> None:
    send(user = instance.user,
        data = {
            'type': 'kafka.message',
             'message': {
                'message_type': NOTIFICATION_DELETE_NOTIFICATION_TYPE, 
                'notification': {
                    'id': instance.id,
                }
            }
        }
    )