from typing import (
    final, 
    Any,
    Optional
)
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.contrib.auth.hashers import (
    make_password,
    check_password,
)
from django.utils.crypto import get_random_string
from datetime import datetime
from django.conf import settings


class ApiKey(models.Model):
    value: str = models.CharField(
        max_length=settings.API_KEY_MAX_LENGTH, null=True, unique=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    expire_time: Optional[datetime]  = models.DateTimeField(null=True)

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
        self.value = self.make_api_key()
        super(ApiKey, self).save(*args, **kwargs)

    class Meta:
        db_table: str = "api_key"
        verbose_name: str = "api key"
        verbose_name_plural: str = "api keys"
        ordering: list[str] = ['-id']