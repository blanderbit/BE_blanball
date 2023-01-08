from os import path
from typing import Optional, final

from authentication.models import (
    User,
    validate_image,
)
from django.conf import settings
from django.db import models
from django.db.models.fields.files import (
    ImageFieldFile,
)
from django.db.models.query import QuerySet
from django.utils import timezone


def bug_image_name(instance: "BugImage", filename: str) -> str:
    datetime = timezone.now().strftime("%Y-%m-%d-%H-%M")
    filename: str = f"{datetime}"
    return path.join("bugs", filename)


class BugImage(models.Model):
    image: Optional[ImageFieldFile] = models.ImageField(
        null=True, upload_to=bug_image_name, validators=[validate_image], default=None
    )

    @property
    def image_url(self) -> Optional[str]:
        if self.image:
            return self.image.url.replace("minio:9000", settings.MINIO_IMAGE_HOST)
        return None

    @final
    def __repr__(self) -> str:
        return "<BugImage %s>" % self.id

    @final
    def __str__(self) -> str:
        return self.image

    class Meta:
        db_table: str = "bug_image"
        verbose_name: str = "bug_image"
        verbose_name_plural: str = "bug_images"


class Bug(models.Model):
    class Type(models.TextChoices):
        CLOSED: str = "Closed"
        CONSIDERATION: str = "Consideration"
        OPEN: str = "Open"

    author: User = models.ForeignKey(User, on_delete=models.CASCADE)
    title: str = models.CharField(max_length=255)
    description: Optional[str] = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    images: Optional[BugImage] = models.ManyToManyField(BugImage, blank=True)
    type: str = models.CharField(choices=Type.choices, max_length=15, default=Type.OPEN)

    @final
    @staticmethod
    def get_all() -> QuerySet["Bug"]:
        return (
            Bug.objects.prefetch_related("images")
            .select_related("author")
            .order_by("-id")
        )

    @final
    def __repr__(self) -> str:
        return "<Bug %s>" % self.id

    @final
    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table: str = "bug"
        verbose_name: str = "bug"
        verbose_name_plural: str = "bugs"
