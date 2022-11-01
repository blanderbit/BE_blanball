from typing import Any, Union

from events.models import (
    Event,
    RequestToParticipation,
    InviteToEvent
)
from events.services import (
    send_notification_to_subscribe_event_user,
)
from events.constant.notification_types import (
    EVENT_DELETE_NOTIFICATION_TYPE, 
    NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE,
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT,
    INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_REQUEST_TO_PARTICIPATION,
    LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
    EVENT_HAS_BEEN_ENDEN_NOTIFICATION_TYPE,
)

from django.db.models.signals import pre_delete, post_save, m2m_changed
from django.dispatch import receiver

from notifications.models import Notification
from notifications.tasks import (
    send_to_user, send
)

from authentication.models import User


def send_to_all_event_users(*, event: Event, message_type: str, data: dict[str, Any]) -> None:
    for user in (list(event.current_users.all()) + [event.author]):
        send_to_user(
            user,
            message_type = message_type,
            data = data
        )

@receiver(m2m_changed, sender = Event.current_users.through)
def send_to_scedular_after_new_user_join_to_event(sender: User, instance: User, **kwargs: Any) -> None:
    action: str = kwargs.pop('action', None)
    if action == 'pre_add':
        event: Event = instance.current_rooms.through.objects.last().event
        if event.current_users.all().count() + 1 == event.amount_members:
            send_to_all_event_users(event = event, message_type = LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
                data = {
                    'event': {
                        'id': event.id,
                        'name': event.name,
                    }
                }
            )


@receiver(post_save, sender = Event)
def delete_event(sender: Event, instance: Event, **kwargs) -> None:
    if instance.status == instance.Status.FINISHED:
        send_to_all_event_users(event = instance, message_type = EVENT_HAS_BEEN_ENDEN_NOTIFICATION_TYPE,
            data = {
                'event': {
                    'id': instance.id,
                    'name': instance.name,
                }
            }
        )

@receiver(pre_delete, sender = Event)
def delete_event(sender: Event, instance: Event, **kwargs) -> None:
    send_notification_to_subscribe_event_user(event = instance,
    message_type = EVENT_DELETE_NOTIFICATION_TYPE)

def send_update_message_after_response(*, instance: Union[InviteToEvent, RequestToParticipation], message_type: str) -> None:
    if instance.status != instance.Status.WAITING:
        try:
            status: dict[str, bool] = {instance.Status.ACCEPTED: True, instance.Status.DECLINED: False}
            notification = Notification.objects.get(message_type = INVITE_USER_TO_EVENT_NOTIFICATION_TYPE, data__invite__id = instance.id)
            send(user = instance.recipient, 
                data = {
                    'type': 'kafka.message',
                    'message': {
                        'message_type': message_type,
                        'notification': {
                            'id': notification.id,
                            'message_type': notification.message_type,
                            'response': status[instance.status]
                        },
                    }
                })
            notification.data.update({'response': status[instance.status]})
            notification.save()
            
        except Notification.DoesNotExist:
            pass



@receiver(post_save, sender = InviteToEvent)
def send_message_after_response_to_invite_to_event(sender: InviteToEvent, instance: InviteToEvent, **kwargs: Any) -> None:
    send_update_message_after_response(instance = instance, message_type = UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT)

@receiver(post_save, sender = RequestToParticipation)
def send_message_after_response_to_request_to_participation(sender: RequestToParticipation, instance: RequestToParticipation, **kwargs: Any) -> None:
    send_update_message_after_response(instance = instance, message_type = UPDATE_MESSAGE_ACCEPT_OR_DECLINE_REQUEST_TO_PARTICIPATION)

@receiver(post_save, sender = RequestToParticipation)
def after_send_request_to_PARTICIPATION(sender: RequestToParticipation, instance: RequestToParticipation, **kwargs: Any) -> None:
    if instance.status == instance.Status.WAITING:
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