from typing import Any, Union

from authentication.models import User
from django.db.models.signals import (
    m2m_changed,
    post_save,
    pre_delete,
)
from django.dispatch import receiver
from events.constants.notification_types import (
    EVENT_DELETE_NOTIFICATION_TYPE,
    EVENT_HAS_BEEN_ENDEN_NOTIFICATION_TYPE,
    INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
    LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
    NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE,
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT,
    UPDATE_MESSAGE_ACCEPT_OR_DECLINE_REQUEST_TO_PARTICIPATION,
    YOU_ARE_LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
)
from events.models import (
    Event,
    InviteToEvent,
    RequestToParticipation,
)
from events.services import (
    send_notification_to_subscribe_event_user,
)
from notifications.models import Notification
from notifications.tasks import send, send_to_user
