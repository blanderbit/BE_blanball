from requests import request
from events.models import (
    Event,
    RequestToParticipation
)
from events.services import (
    send_notification_to_subscribe_event_user,
    send_to_user,
)
from events.constants import (
    EVENT_DELETE_MESSAGE_TYPE, NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE
)

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from events.middlewares import current_request


@receiver(pre_delete, sender = Event)
def delete_event(sender: Event, instance, **kwargs) -> None:
    send_notification_to_subscribe_event_user(event = instance,
    message_type = EVENT_DELETE_MESSAGE_TYPE)


@receiver(post_save, sender = RequestToParticipation)
def after_send_request_to_PARTICIPATION(sender: RequestToParticipation, instance, **kwargs) -> None:
    send_to_user(user = instance.event.author,
    message_type = NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE, 
    data = {
    'recipient': {
        'id': instance.event.author.id, 
        'name': instance.event.author.profile.name, 
        'last_name': instance.event.author.profile.last_name,
    },
    'request': {
        'id': instance.id
    },
    'sender': {
        'id': current_request().user, 
        'name': current_request().user.profile.name, 
        'last_name': current_request().user.profile.last_name,
    },
    'event': {
        'id': instance.event.id
    }
})