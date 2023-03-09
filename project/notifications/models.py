from datetime import datetime
from typing import Any, final

from authentication.models import User
from django.db import models
from django.db.models.query import QuerySet


class Notification(models.Model):
    class Type(models.TextChoices):
        UNREAD: str = "Unread"
        READ: str = "Read"

    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    type: str = models.CharField(
        choices=Type.choices, max_length=6, default=Type.UNREAD
    )
    time_created: datetime = models.DateTimeField(auto_now_add=True)
    message_type: str = models.CharField(max_length=100)
    data: dict[str, Any] = models.JSONField()

    @final
    def __repr__(self) -> str:
        return "<Notification %s>" % self.id

    @final
    @staticmethod
    def get_all() -> QuerySet["Notification"]:
        """
        getting all records with optimized selection from the database
        """
        return Notification.objects.select_related("user")

    @final
    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "notification"
        verbose_name: str = "notification"
        verbose_name_plural: str = "notifications"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
