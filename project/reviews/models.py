from datetime import datetime
from typing import final

from authentication.models import User
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models.query import QuerySet
from events.models import Event


@final
class Review(models.Model):
    author: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author",
        db_index=True
    )
    text: str = models.CharField(max_length=200)
    time_created: datetime = models.DateTimeField(auto_now_add=True)
    stars: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    user: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews",
        db_index=True
    )

    def __repr__(self) -> str:
        return "<Review %s>" % self.id

    @staticmethod
    def get_all() -> QuerySet["Review"]:
        """
        getting all records with optimized selection from the database
        """
        return Review.objects.select_related("user", "author")

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "review"
        verbose_name: str = "review"
        verbose_name_plural: str = "reviews"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]


@final
class EventReview(models.Model):
    author: User = models.ForeignKey(User, on_delete=models.CASCADE)
    text: str = models.CharField(max_length=200, null=True)
    time_created: datetime = models.DateTimeField(auto_now_add=True)
    stars: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    event: Event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return "<EventReview %s>" % self.id

    @staticmethod
    def get_all() -> QuerySet["EventReview"]:
        """
        getting all records with optimized selection from the database
        """
        return EventReview.objects.select_related("user", "event")

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        # the name of the table in the database for this model
        db_table: str = "event_review"
        verbose_name: str = "event review"
        verbose_name_plural: str = "event reviews"
        # sorting database records for this model by default
        ordering: list[str] = ["-id"]
