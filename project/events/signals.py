from typing import Any

from events.models import (
    Event,
    RequestToParticipation
)
from events.services import (
    send_notification_to_subscribe_event_user,
)
from events.constant.notification_types import (
    EVENT_DELETE_NOTIFICATION_TYPE, NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE
)

from notifications.tasks import (
    send_to_scedular, send_to_user
)
from django.db.models.signals import pre_delete, post_save, m2m_changed
from django.dispatch import receiver

from authentication.models import User


@receiver(pre_delete, sender = Event)
def delete_event(sender: Event, instance: Event, **kwargs: Any) -> None:
    send_notification_to_subscribe_event_user(event = instance,
    message_type = EVENT_DELETE_NOTIFICATION_TYPE)


@receiver(pre_delete, sender = Event)
def send_to_scedular_before_delete_event(sender: Event, instance: Event, **kwargs: Any) -> None:
    for user in ((list(instance.current_users.all()) + list(instance.current_fans.all())) + [instance.author]):
        send_to_scedular(user = user, data = {'event': {'id': instance, 'type': 'deleted'}})



@receiver(post_save, sender = Event)
def send_to_scedular_after_create_event(sender: Event, instance: Event, **kwargs: Any) -> None:
    send_to_scedular(user = instance.author, data = {'event': {'data': str(instance.__dict__), 'type': 'new_event'}})


@receiver(m2m_changed, sender = Event.current_users.through)
def send_to_scedular_after_new_user_join_to_event(sender: User, instance: User, **kwargs: Any) -> None:
    action: str = kwargs.pop('action', None)
    if action == 'post_add':
        event: Event = instance.current_rooms.through.objects.last().event
        send_to_scedular(user = instance, data = {'event': {'data': str(event.__dict__), 
            'type': 'new_event'}})
        print(str(event.__dict__))
        for user in ((list(event.current_users.all()) + list(event.current_fans.all())) + [event.author]):
            send_to_scedular(user = user, data = {'event': {'id': event.id, 'type': 'new_user', 'count_users': event.current_users.all().count()}})


@receiver(post_save, sender = RequestToParticipation)
def after_send_request_to_PARTICIPATION(sender: RequestToParticipation, instance, **kwargs) -> None:
    send_to_user(user = instance.recipient,
    message_type = NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE, 
    data = {
        'recipient': {
            'id': instance.recipient.id, 
            'name': instance.recipient.profile.name, 
            'last_name': instance.recipient.profile.last_name,
        },
        'request': {
            'id': instance.id
        },
        'sender': {
            'id': instance.sender.id, 
            'name': instance.sender.profile.name, 
            'last_name': instance.sender.profile.last_name,
        },
        'event': {
            'id': instance.event.id,
            'name': instance.event.name,
        }
    })