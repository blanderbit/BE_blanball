from typing import final
from datetime import (
    datetime
)

from django.db import models
from django.db.models.query import QuerySet


@final
class Hint(models.Model):
    name: str = models.CharField(max_length=255, unique=True)
    time_created: datetime = models.DateTimeField(auto_now_add=True)

    @final
    def __repr__(self) -> str:
        return "<UserHint %s>" % self.id

    @final
    def __str__(self) -> str:
        return self.name

    @final
    @staticmethod
    def get_all() -> QuerySet["Hint"]:
        """
        getting all records with optimized selection from the database
        """
        return Hint.objects.all()

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "hint"
        verbose_name: str = "hint"
        verbose_name_plural: str = "hints"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
