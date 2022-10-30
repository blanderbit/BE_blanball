from typing import Any

from events.models import (
    Event,
    RequestToParticipation,
    InviteToEvent
)
from events.services import (
    send_notification_to_subscribe_event_user,
)
from events.constant.notification_types import (
    EVENT_DELETE_NOTIFICATION_TYPE, NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE,
    RESPONSE_TO_THE_INVITE_TO_EVENT_NOTIFICATION_TYPE,
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT,
    INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
)

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from notifications.models import Notification
from notifications.tasks import (
    send_to_user, send
)
from authentication.models import User

@receiver(pre_delete, sender = Event)
def delete_event(sender: Event, instance: Event, **kwargs) -> None:
    send_notification_to_subscribe_event_user(event = instance,
    message_type = EVENT_DELETE_NOTIFICATION_TYPE)

print(Notification.objects.filter(message_type = INVITE_USER_TO_EVENT_NOTIFICATION_TYPE).last().data)

@receiver(post_save, sender = InviteToEvent)
def send_message_after_response_to_invite(sender: InviteToEvent, instance: InviteToEvent, **kwargs: Any) -> None:
    if instance.status != instance.Status.WAITING:
        try:
            status: dict[str, bool] = {instance.Status.ACCEPTED: True, instance.Status.DECLINED: False}
            notification = Notification.objects.get(message_type = INVITE_USER_TO_EVENT_NOTIFICATION_TYPE, data__invite__id = instance.id)
            send(user = instance.recipient, 
                data = {
                    'type': 'kafka.message',
                    'notification': {
                        'id': notification.id,
                        'message_type': notification.message_type,
                        'response': status[instance.status]
                    },
                    'new_message_type': UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT,
                })
        except Notification.DoesNotExist:
            pass



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