from events.models import Event
from events.services import send_notification_to_subscribe_event_user
from events.constaints import (EVENT_DELETE_MESSAGE_TYPE, EVENT_DELETE_TEXT)

from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender = Event)
def delete_event(sender: Event, instance, **kwargs) -> None:
    send_notification_to_subscribe_event_user(event = instance, notification_text = 
    EVENT_DELETE_TEXT.format(event_id = instance.id ),
    message_type = EVENT_DELETE_MESSAGE_TYPE)
