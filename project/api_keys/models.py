from datetime import datetime
from typing import Any, Optional, final

from api_keys.constants.errors import (
    API_KEY_BAD_EXPIRE_TIME_ERROR,
)
from django.conf import settings
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


class ApiKey(models.Model):
    value: str = models.CharField(
        max_length=settings.API_KEY_MAX_LENGTH, null=True, unique=True
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    expire_time: Optional[datetime] = models.DateTimeField(null=True)

    @final
    def __repr__(self) -> str:
        return "<ApiKey %s>" % self.id

    @final
    def get_only_active() -> QuerySet["ApiKey"]:
        return ApiKey.objects.filter(expire_time__gt=timezone.now())

    @final
    def get_only_expired() -> QuerySet["ApiKey"]:
        return ApiKey.objects.filter(expire_time__lt=timezone.now())

    @final
    def __str__(self) -> str:
        return self.value

    @final
    def make_api_key(self) -> str:
        return get_random_string(settings.API_KEY_MAX_LENGTH)

    @final
    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.expire_time < timezone.now():
            raise ValidationError(API_KEY_BAD_EXPIRE_TIME_ERROR, HTTP_400_BAD_REQUEST)
        self.value = self.make_api_key()
        super(ApiKey, self).save(*args, **kwargs)

    class Meta:
        db_table: str = "api_key"
        verbose_name: str = "api key"
        verbose_name_plural: str = "api keys"
        ordering: list[str] = ["-id"]
