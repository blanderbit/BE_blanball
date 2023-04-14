from typing import (
    final
)
from datetime import (
    datetime
)

from django.db.models.query import QuerySet
from django.db import models

from authentication.models import User


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