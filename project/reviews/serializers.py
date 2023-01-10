from collections import OrderedDict
from typing import Any, Union

from authentication.models import User
from authentication.serializers import (
    ReviewAuthorSerializer,
)
from notifications.tasks import send_to_user
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)
from reviews.constants.errors import (
    REVIEW_CREATE_ERROR,
)
from reviews.constants.notification_types import (
    REVIEW_CREATE_NOTIFICATION_TYPE,
)
from reviews.models import EventReview, Review


class CreateReviewSerializer(ModelSerializer):
    class Meta:
        model: Review = Review
        exclude: Union[str, list[str]] = [
            "author",
        ]

    def validate(self, attrs) -> OrderedDict:
        user: User = attrs.get("user")

        if self.context["request"].user.email == user.email:
            raise ValidationError(REVIEW_CREATE_ERROR, HTTP_400_BAD_REQUEST)
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Review:
        user: User = User.get_all().get(email=validated_data["user"])
        review: Review = Review.objects.create(
            author=self.context["request"].user, **validated_data
        )
        send_to_user(
            user=user,
            message_type=REVIEW_CREATE_NOTIFICATION_TYPE,
            data={
                "recipient": {
                    "id": review.user.id,
                    "name": review.user.profile.name,
                    "last_name": review.user.profile.last_name,
                    "avatar": review.user.profile.avatar_url,
                },
                "review": {
                    "id": review.id,
                },
                "sender": {
                    "id": review.author.id,
                    "name": review.author.profile.name,
                    "last_name": review.author.profile.last_name,
                    "avatar": review.author.profile.avatar_url,
                },
            },
        )
        user: User = User.get_all().get(email=validated_data["user"])
        stars = 0
        for item in user.reviews.all():
            stars += item.stars
        user.raiting = stars / user.reviews.count()
        user.save()
        return review


class ReviewListSerializer(ModelSerializer):
    author = ReviewAuthorSerializer()

    class Meta:
        model: Review = Review
        exclude: Union[str, list[str]] = [
            "user",
        ]


class CreateEventReviewSerializer(ModelSerializer):
    class Meta:
        model: EventReview = EventReview
        exclude: Union[str, list[str]] = ["author", "time_created"]
