from typing import (
    final
)
from datetime import (
    datetime
)
from friends.constants.notification_types import (
    INVITE_USER_TO_FRIENDS_NOTIFICATION_TYPE
)
from friends.constants.errors import (
    ALREADY_SENT_REQUEST_TO_THIS_USER_IN_FRIENDS,
    CAN_NOT_INVITE_YOURSELF_TO_FRIENDS
)
from authentication.models import User

from django.db.models.query import QuerySet
from django.db import models
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
)
from rest_framework.serializers import (
    ValidationError,
)
from notifications.tasks import (
    send_to_user
)

class Friend(models.Model):
    user: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user"
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    friend: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend"
    )

    @final
    @staticmethod
    def get_all() -> QuerySet["Friend"]:
        """
        getting all records with optimized selection from the database
        """
        return Friend.objects.select_related("user", "friend")

    @final
    def __repr__(self) -> str:
        return "<Friend %s>" % self.id

    @final
    def __str__(self) -> str:
        return self.user.profile.name
    
    class Meta:
        # the name of the table in the database for this model
        db_table: str = "friend"
        verbose_name: str = "friend"
        verbose_name_plural: str = "friends"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]



class InviteToFriendsManager(models.Manager):
    def send_invite(
        self, request_user: User, invite_user: User
    ) -> "InviteToFriends":

        if invite_user.id == request_user.id:
            raise ValidationError(CAN_NOT_INVITE_YOURSELF_TO_FRIENDS, HTTP_403_FORBIDDEN)
        if (
            InviteToFriends.get_all()
            .filter(
                recipient=invite_user, sender=request_user
            )
            .exists()
        ):
            raise ValidationError(ALREADY_SENT_REQUEST_TO_THIS_USER_IN_FRIENDS, HTTP_403_FORBIDDEN)
        invite = self.model(recipient=invite_user, sender=request_user)
        invite.save()
        send_to_user(
            user=invite_user,
            message_type=INVITE_USER_TO_FRIENDS_NOTIFICATION_TYPE,
            data={
                "recipient": {
                    "id": invite_user.id,
                    "name": invite_user.profile.name,
                    "last_name": invite_user.profile.last_name,
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


class InviteToFriends(models.Model):
    class Status(models.TextChoices):
        WAITING: str = "Waiting"
        ACCEPTED: str = "Accepted"
        DECLINED: str = "Declined"

    recipient: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invite_recipient"
    )
    time_created: datetime = models.DateTimeField(auto_now_add=True)
    sender: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invite_sender"
    )
    status: str = models.CharField(
        choices=Status.choices, max_length=10, default=Status.WAITING
    )

    def __repr__(self) -> str:
        return "<InviteToFriends %s>" % self.id

    def __str__(self) -> str:
        return str(self.id)

    @staticmethod
    def get_all() -> QuerySet["InviteToFriends"]:
        """
        getting all records with optimized selection from the database
        """
        return InviteToFriends.objects.select_related(
            "sender", "sender"
        )

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "invite_to_friends"
        verbose_name: str = "invite to friends"
        verbose_name_plural: str = "invites to friends"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]