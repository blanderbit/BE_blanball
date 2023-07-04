
from typing import final
from authentication.models import User
from events.models.event_model import (
    Event
)
from events.models.invite_to_event_model import (
    RequestToParticipation
)
from django.db import models
from django.db.models.query import QuerySet
from events.constants.errors import (
    AUTHOR_CAN_NOT_INVITE_ERROR,
    CAN_NOT_INVITE_YOURSELF,
    THIS_USER_CAN_NOT_BE_INVITED,
    USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR,
)
from events.constants.notification_types import (
    INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
)
from notifications.tasks import send_to_user
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
)


class InviteToEventManager(models.Manager):
    def send_invite(
        self, request_user: User, invite_user: User, event: Event
    ) -> "InviteToEvent":

        if invite_user.id == request_user.id:
            raise ValidationError(CAN_NOT_INVITE_YOURSELF, HTTP_403_FORBIDDEN)
        if invite_user.id == event.author.id:
            raise ValidationError(AUTHOR_CAN_NOT_INVITE_ERROR, HTTP_403_FORBIDDEN)
        if invite_user in event.black_list.all():
            raise ValidationError(THIS_USER_CAN_NOT_BE_INVITED, HTTP_403_FORBIDDEN)
        if InviteToEvent.get_all().filter(recipient=invite_user, event=event).exists():
            raise ValidationError(THIS_USER_CAN_NOT_BE_INVITED, HTTP_403_FORBIDDEN)

        if (
            request_user.id == event.author.id
            or request_user in event.current_users.all()
        ):
            invite = self.model(recipient=invite_user, event=event, sender=request_user)
            invite.save()
            send_to_user(
                user=invite_user,
                message_type=INVITE_USER_TO_EVENT_NOTIFICATION_TYPE,
                data={
                    "recipient": {
                        "id": invite_user.id,
                        "name": invite_user.profile.name,
                        "last_name": invite_user.profile.last_name,
                    },
                    "event": {
                        "id": event.id,
                        "name": event.name,
                        "date_and_time": str(event.date_and_time),
                    },
                    "invite": {
                        "id": invite.id,
                    },
                    "sender": {
                        "id": request_user.id,
                        "name": request_user.profile.name,
                        "last_name": request_user.profile.last_name,
                    },
                },
            )
            return invite
        else:
            raise ValidationError(
                USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR, HTTP_403_FORBIDDEN
            )


@final
class InviteToEvent(RequestToParticipation):

    objects = InviteToEventManager()

    def __repr__(self) -> str:
        return "<InviteToEvent %s>" % self.id

    def __str__(self) -> str:
        return str(self.id)

    @staticmethod
    def get_all() -> QuerySet["InviteToEvent"]:
        """
        getting all records with optimized selection from the database
        """
        return InviteToEvent.objects.select_related("recipient", "event", "sender")

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "invite_to_event"
        verbose_name: str = "invite to event"
        verbose_name_plural: str = "invites to event"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
