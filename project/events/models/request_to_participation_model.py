from datetime import datetime

from authentication.models import User
from events.models.event_model import (
    Event
)
from django.db import models
from django.db.models.query import QuerySet


class RequestToParticipation(models.Model):
    class Status(models.TextChoices):
        WAITING: str = "Waiting"
        ACCEPTED: str = "Accepted"
        DECLINED: str = "Declined"

    recipient: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipient"
    )
    time_created: datetime = models.DateTimeField(auto_now_add=True)
    event: Event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="invites"
    )
    sender: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender"
    )
    status: str = models.CharField(
        choices=Status.choices, max_length=10, default=Status.WAITING
    )

    def __repr__(self) -> str:
        return "<RequestToParticipation %s>" % self.id

    def __str__(self) -> str:
        return str(self.id)

    @staticmethod
    def get_all() -> QuerySet["RequestToParticipation"]:
        """
        getting all records with optimized selection from the database
        """
        return RequestToParticipation.objects.select_related(
            "recipient", "event", "sender"
        )

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "request_to_participation"
        verbose_name: str = "request to participation"
        verbose_name_plural: str = "requests to participation"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
