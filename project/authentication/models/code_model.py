from datetime import datetime
from typing import Optional, final

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


@final
class Code(models.Model):
    verify_code: str = models.CharField(max_length=5, unique=True)
    life_time: datetime = models.DateTimeField(null=True)
    type: str = models.CharField(max_length=20)
    user_email: str = models.CharField(max_length=255)
    dop_info: Optional[str] = models.CharField(max_length=255, null=True)

    def get_only_expired() -> QuerySet["Code"]:
        """
        get all expired codes
        """
        return Code.objects.filter(life_time__lt=timezone.now())

    def __repr__(self) -> str:
        return "<Code %s>" % self.id

    def __str__(self) -> str:
        return self.verify_code

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "code"
        verbose_name: str = "code"
        verbose_name_plural: str = "codes"
