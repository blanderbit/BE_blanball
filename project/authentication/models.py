import os
from datetime import date, datetime
from typing import Any, Optional, Union, final

from authentication.constants.errors import (
    AVATAR_MAX_SIZE_ERROR,
    MAX_AGE_VALUE_ERROR,
    MIN_AGE_VALUE_ERROR,
)
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.contrib.gis.db.models import (
    PointField,
)
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import (
    TemporaryUploadedFile,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models, transaction
from django.db.models.fields.files import (
    ImageFieldFile,
)
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import smart_bytes
from django.utils.http import (
    urlsafe_base64_encode,
)
from hints.models import Hint
from phonenumber_field.modelfields import (
    PhoneNumberField,
)
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)
from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken,
)


class UserManager(BaseUserManager):
    @final
    def create_user(
        self, email: str, phone: str, password: None = None, *agrs: Any, **kwargs: Any
    ) -> "User":
        user = self.model(
            phone=phone, email=self.normalize_email(email), *agrs, **kwargs
        )
        user.set_password(password)
        user.role = "User"
        user.save()
        return user


class Gender(models.TextChoices):
    MAN: str = "Man"
    WOMAN: str = "Woman"


def validate_birthday(value: date) -> None:
    """
    validation of a user-entered date of birth ranging from 6 to 80 years
    """
    if timezone.now().date() - value > timezone.timedelta(days=29200):
        raise ValidationError(MAX_AGE_VALUE_ERROR, HTTP_400_BAD_REQUEST)
    if timezone.now().date() - value < timezone.timedelta(days=2191):
        raise ValidationError(MIN_AGE_VALUE_ERROR, HTTP_400_BAD_REQUEST)


@final
def configuration_dict() -> dict[str, bool]:
    """
    the default configuration field value for the user
    """
    return {"email": True, "phone": True, "show_reviews": True}


def image_file_name(instance: "Profile", filename: str) -> str:
    """
    setting the name for the avatar uploaded by the user
    """
    return os.path.join("users", str(filename))


def validate_image(image: TemporaryUploadedFile) -> str:
    """
    validation of the image uploaded by the user by the maximum size value
    """
    megabyte_limit: float = 1.0
    if image.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(AVATAR_MAX_SIZE_ERROR, HTTP_400_BAD_REQUEST)

