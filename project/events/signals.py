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
    EVENT_DELETE_MESSAGE_TYPE, EVENT_DELETE_TEXT, NEW_REQUEST_TO_PARTICIPATION, NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE
)

from django.db.models.signals import pre_delete, post_save, m2m_changed, pre_save
from django.dispatch import receiver

from events.middlewares import current_request


@receiver(pre_delete, sender = Event)
def delete_event(sender: Event, instance, **kwargs) -> None:
    send_notification_to_subscribe_event_user(event = instance, notification_text = 
    EVENT_DELETE_TEXT.format(event_id = instance.id ),
    message_type = EVENT_DELETE_MESSAGE_TYPE)


@receiver(post_save, sender = RequestToParticipation)
def after_send_request_to_PARTICIPATION(sender: RequestToParticipation, instance, **kwargs) -> None:
    print(current_request().user)
    send_to_user(user = instance.event.author, notification_text =
    NEW_REQUEST_TO_PARTICIPATION.format(author_name = instance.event.author.profile.name, event_id = instance.event.id),
    message_type = NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE, data = {'event_id': instance.event.id, 'user_id': current_request().user.id})

