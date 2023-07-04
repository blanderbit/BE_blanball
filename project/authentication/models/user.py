from typing import Any, Optional, final
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models
from django.db.models.query import QuerySet
from hints.models import Hint
from phonenumber_field.modelfields import (
    PhoneNumberField,
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


@final
def configuration_dict() -> dict[str, bool]:
    """
    the default configuration field value for the user
    """
    return {"email": True, "phone": True, "show_reviews": True}


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
