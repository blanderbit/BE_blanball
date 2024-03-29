from os import path
from typing import Optional, final

from authentication.models import User
from authentication.models.profile_model import (
    validate_image,
)
from django.conf import settings
from django.db import models
from django.db.models.fields.files import (
    ImageFieldFile,
)
from django.db.models.query import QuerySet
from django.utils import timezone


@final
def bug_image_name(instance: "BugImage", filename: str) -> str:
    """
    setting the name for uploaded bug report image
    """
    datetime = timezone.now().strftime("%Y-%m-%d-%H-%M")
    filename: str = f"{datetime}"
    return path.join("bugs", filename)


@final
class BugImage(models.Model):
    image: Optional[ImageFieldFile] = models.ImageField(
        null=True, upload_to=bug_image_name, validators=[validate_image], default=None
    )

    @property
    def image_url(self) -> Optional[str]:
        """
        Getting the correct path to the image.
        This replaces the default image host "minio:9000" with
        the host where the image storage is located.
        """
        if self.image:
            return self.image.url.replace("minio:9000", settings.MINIO_IMAGE_HOST)
        return None

    def __repr__(self) -> str:
        return "<BugImage %s>" % self.id

    def __str__(self) -> str:
        return self.image

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "bug_image"
        verbose_name: str = "bug_image"
        verbose_name_plural: str = "bug_images"


@final
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

    @staticmethod
    def get_all() -> QuerySet["Bug"]:
        """
        getting all records with optimized selection from the database
        """
        return Bug.objects.prefetch_related("images").select_related("author")

    def __repr__(self) -> str:
        return "<Bug %s>" % self.id

    def __str__(self) -> str:
        return self.title

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "bug"
        verbose_name: str = "bug"
        verbose_name_plural: str = "bugs"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
