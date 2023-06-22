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


@final
class Profile(models.Model):
    class Position(models.TextChoices):
        GK: str = "GK"
        LB: str = "LB"
        RB: str = "RB"
        CB: str = "CB"
        LWB: str = "LWB"
        RWB: str = "RWB"
        CDM: str = "CDM"
        CM: str = "CM"
        CAM: str = "CAM"
        RM: str = "RM"
        LM: str = "LM"
        RW: str = "RW"
        LW: str = "LW"
        RF: str = "RF"
        CF: str = "CF"
        LF: str = "LF"
        ST: str = "ST"

    class Leg(models.TextChoices):
        LEFT: str = "Left"
        RIGHT: str = "Right"

    name: str = models.CharField(max_length=20, db_index=True)
    last_name: str = models.CharField(max_length=20, db_index=True)
    gender: Optional[str] = models.CharField(
        choices=Gender.choices, max_length=10, null=True
    )
    birthday: Optional[date] = models.DateField(
        null=True, validators=[validate_birthday]
    )
    avatar: Optional[ImageFieldFile] = models.ImageField(
        null=True, upload_to=image_file_name, validators=[validate_image], default=None
    )
    age: Optional[int] = models.PositiveSmallIntegerField(null=True)
    height: Optional[int] = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ],
    )
    weight: Optional[int] = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ],
    )
    position: Optional[str] = models.CharField(
        choices=Position.choices, max_length=255, null=True
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    about_me: Optional[str] = models.CharField(null=True, blank=True, max_length=110)
    working_leg: Optional[str] = models.CharField(
        choices=Leg.choices, max_length=255, null=True
    )
    place: Optional[dict[str, Union[str, float]]] = models.JSONField(null=True, db_index=True)
    coordinates: Optional[Point] = PointField(null=True, srid=4326)

    def __repr__(self) -> str:
        return "<Profile %s>" % self.id

    def __str__(self) -> str:
        return self.name

    @transaction.atomic
    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.place != None:
            self.coordinates = Point(self.place["lon"], self.place["lat"])
        super(Profile, self).save(*args, **kwargs)
        from authentication.services import (
            update_user_profile_avatar,
        )

        update_user_profile_avatar(avatar=self.avatar, profile_id=self.id)

    @property
    def new_image_name(self) -> str:
        """
        Generates a new name for the picture the user has uploaded.
        The new picture will consist of the encoded user id and the current date
        """
        datetime = timezone.now().strftime("%Y-%m-%d-%H-%M")
        return f"users/{urlsafe_base64_encode(smart_bytes(self.id))}_{datetime}.jpg"

    @property
    def avatar_url(self) -> Optional[str]:
        """
        Getting the correct path to the image.
        This replaces the default image host "minio:9000" with
        the host where the image storage is located.
        """
        if self.avatar:
            return self.avatar.url.replace(
                f'http://{os.getenv("FILE_STORAGE_ENDPOINT")}',
                settings.MINIO_IMAGE_HOST,
            )
        return None

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "profile"
        verbose_name: str = "profile"
        verbose_name_plural: str = "profiles"


@final
class User(AbstractBaseUser):
    class Role(models.TextChoices):
        USER: str = "User"
        ADMIN: str = "Admin"

    email: str = models.EmailField(max_length=255, unique=True, db_index=True)
    phone: str = PhoneNumberField(unique=True)
    is_verified: bool = models.BooleanField(default=False)
    is_online: bool = models.BooleanField(default=False, db_index=True)
    get_planned_events: str = models.CharField(max_length=10, default="1m")
    role: str = models.CharField(choices=Role.choices, max_length=10, null=True)
    updated_at: str = models.DateTimeField(auto_now=True)
    raiting: Optional[float] = models.FloatField(null=True)
    profile: Profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name="user"
    )
    configuration: dict[str, bool] = models.JSONField(default=configuration_dict)
    checked_hints: list[Optional[Hint]] = models.ManyToManyField(Hint, blank=True)

    USERNAME_FIELD: str = "email"

    objects = UserManager()

    def __repr__(self) -> str:
        return "<User %s>" % self.id

    def __str__(self) -> str:
        return self.email

    @staticmethod
    def get_all() -> QuerySet["User"]:
        """
        getting all records with optimized selection from the database
        """
        return User.objects.select_related("profile")

    def tokens(self) -> dict[str, str]:
        """
        generating jwt tokens for user object
        """
        refresh: RefreshToken = RefreshToken.for_user(self)
        access: AccessToken = AccessToken.for_user(self)
        return {"refresh": str(refresh), "access": str(access)}

    @property
    def count_pinned_events(self) -> int:
        from events.models import Event

        return Event.get_all().filter(author_id=self.id, pinned=True).count()

    @property
    def group_name(self) -> str:
        return "user_%s" % self.id

    @property
    def chat_group_name(self) -> str:
        return "chat_user_%s" % self.id

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "user"
        verbose_name: str = "user"
        verbose_name_plural: str = "users"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]


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
