from os import path
from typing import Optional

from authentication.models import (
    User,
    validate_image,
)
from django.db import models
from django.db.models.fields.files import (
    ImageFieldFile,
)


def bug_image_name(instance: "Bug", filename: str) -> str:
    time_created: str = instance.time_created.strftime("%Y-%m-%d-%H-%M")
    filename: str = f"author_{instance.author.id}_{time_created}"
    return path.join("bugs", filename)


class Bug(models.Model):
    class Type(models.TextChoices):
        CLOSED: str = "Closed"
        OPEN: str = "Open"

    author: User = models.ForeignKey(User, on_delete=models.CASCADE)
    title: str = models.CharField(max_length=255)
    description: Optional[str] = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    image: Optional[ImageFieldFile] = models.ImageField(
        null=True, upload_to=bug_image_name, validators=[validate_image], default=None
    )
    type: str = models.CharField(choices=Type.choices, max_length=10, default=Type.OPEN)
