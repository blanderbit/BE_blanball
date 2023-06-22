from datetime import datetime
from typing import Any, Optional, final

from api_keys.constants.errors import (
    API_KEY_BAD_EXPIRE_TIME_ERROR,
)
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


@final
class ApiKey(models.Model):
    value: str = models.CharField(
        max_length=settings.API_KEY_MAX_LENGTH, null=True, unique=True,
        db_index=True
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    expire_time: Optional[datetime] = models.DateTimeField(
        null=True, db_index=True
    )
    name: str = models.CharField(max_length=55, unique=True)

    def get_only_active() -> QuerySet["ApiKey"]:
        return ApiKey.objects.filter(
            Q(expire_time__gt=timezone.now()) | Q(expire_time=None)
        )

    def get_only_expired() -> QuerySet["ApiKey"]:
        return ApiKey.objects.filter(expire_time__lt=timezone.now())

    def check_api_key_status(api_key: "ApiKey") -> bool:
        try:
            return api_key.expire_time > timezone.now()
        except TypeError:
            return True

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return "<ApiKey %s>" % self.id

    def make_api_key(self) -> str:
        return get_random_string(settings.API_KEY_MAX_LENGTH)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.expire_time and self.expire_time < timezone.now():
            raise ValidationError(API_KEY_BAD_EXPIRE_TIME_ERROR, HTTP_400_BAD_REQUEST)
        self.value = self.make_api_key()
        super(ApiKey, self).save(*args, **kwargs)

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "api_key"
        verbose_name: str = "api key"
        verbose_name_plural: str = "api keys"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
