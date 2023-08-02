from datetime import datetime
from typing import Any, Optional, Union, final

from authentication.models import Gender, User
from django.contrib.gis.db.models import (
    PointField,
)
from django.contrib.gis.geos import Point
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models.query import QuerySet
from events.middlewares import current_request
from phonenumber_field.modelfields import (
    PhoneNumberField,
)


@final
class Event(models.Model):
    class Type(models.TextChoices):
        FOOTBALL: str = "Football"
        FUTSAL: str = "Futsal"

    class CloseType(models.TextChoices):
        SHIRT_FRONT: str = "Shirt-Front"
        T_SHIRT: str = "T-Shirt"
        ANY: str = "Any"

    class Status(models.TextChoices):
        PLANNED: str = "Planned"
        ACTIVE: str = "Active"
        FINISHED: str = "Finished"

    class Duration(models.IntegerChoices):
        MINUTES_10: int = 10
        MINUTES_20: int = 20
        MINUTES_30: int = 30
        MINUTES_40: int = 40
        MINUTES_50: int = 50
        MINUTES_60: int = 60
        MINUTES_70: int = 70
        MINUTES_80: int = 80
        MINUTES_90: int = 90
        MINUTES_100: int = 100
        MINUTES_110: int = 110
        MINUTES_120: int = 120
        MINUTES_130: int = 130
        MINUTES_140: int = 140
        MINUTES_150: int = 150
        MINUTES_160: int = 160
        MINUTES_170: int = 170
        MINUTES_180: int = 180

    author: User = models.ForeignKey(User, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=255, db_index=True)
    description: str = models.TextField()
    place: dict[str, Union[str, float]] = models.JSONField()
    gender: str = models.CharField(choices=Gender.choices, max_length=10)
    date_and_time: datetime = models.DateTimeField()
    contact_number: str = PhoneNumberField(null=True)
    need_ball: bool = models.BooleanField()
    amount_members: int = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(50)], default=6
    )
    type: str = models.CharField(choices=Type.choices, max_length=15)
    price: Optional[int] = models.PositiveSmallIntegerField(
        null=True, validators=[MinValueValidator(1)]
    )
    price_description: Optional[str] = models.CharField(max_length=265, null=True)
    need_form: bool = models.BooleanField()
    privacy: bool = models.BooleanField()
    pinned: bool = models.BooleanField(default=False, db_index=True)
    hidden: bool = models.BooleanField(default=False)
    duration: int = models.PositiveSmallIntegerField(choices=Duration.choices)
    forms: str = models.JSONField(null=True)
    status: str = models.CharField(
        choices=Status.choices, max_length=10, default=Status.PLANNED
    )
    current_users: list[Optional[User]] = models.ManyToManyField(
        User, related_name="current_rooms", blank=True, db_index=True
    )
    current_fans: list[Optional[User]] = models.ManyToManyField(
        User, related_name="current_views_rooms", blank=True, db_index=True
    )
    black_list: list[Optional[User]] = models.ManyToManyField(
        User, related_name="black_list", blank=True, db_index=True
    )
    coordinates: Point = PointField(null=True, srid=4326)

    @property
    def count_current_users(self) -> int:
        """
        getting the count of participants in the event
        """
        return self.current_users.count()

    @property
    def count_current_fans(self) -> int:
        """
        getting the count of fans in the event
        """
        return self.current_fans.count()

    def __repr__(self) -> str:
        return "<Event %s>" % self.id

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_all() -> QuerySet["Event"]:
        """
        getting all records with optimized selection from the database
        """
        return Event.objects.select_related("author").prefetch_related(
            "current_users", "current_fans", "black_list"
        )

    def user_role(self, pk: Optional[int] = None):
        from events.models.request_to_participation_model import (
            RequestToParticipation
        )

        if pk:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                pass
        else:
            request = current_request()
            user = request.user

        event_requests_to_participations = RequestToParticipation.get_all().filter(
            event_id=self.id, status=RequestToParticipation.Status.WAITING
        )
        sender_ids = [d.sender.id for d in event_requests_to_participations]

        if user == self.author:
            return "author"
        elif user in self.current_users.all():
            return "player"
        elif user in self.current_fans.all():
            return "fan"
        elif user.id in sender_ids:
            return "request_participation"
        return None

    @property
    def request_user_role(self) -> Optional[str]:
        return self.user_role()

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.place != None:
            self.coordinates = Point(self.place["lon"], self.place["lat"])
        super(Event, self).save(*args, **kwargs)

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "event"
        verbose_name: str = "event"
        verbose_name_plural: str = "events"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]