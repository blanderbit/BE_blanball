from events.models import Event
from events.services import send_notification_to_subscribe_event_user
from events.constaints import EVENT_DELETE_MESSAGE_TYPE

from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender = Event)
def delete_event(sender, instance, *args, **kwargs):
    send_notification_to_subscribe_event_user(event = instance, notification_text = 'event_deleted',
    message_type = EVENT_DELETE_MESSAGE_TYPE)
