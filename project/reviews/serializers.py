from typing import Any, Union
from collections import OrderedDict

from reviews.models import Review
from authentication.models import User

from reviews.constants import (
    REVIEW_CREATE_ERROR, REVIEW_CREATE_MESSAGE_TYPE,
)
from notifications.tasks import send_to_user

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)


class CreateReviewSerializer(ModelSerializer):
    class Meta:
        model: Review = Review
        exclude: Union[str, list[str]] = [
            'email', 
        ]

    def validate(self, attrs) -> OrderedDict:
        user: User = attrs.get('user')
    
        if self.context['request'].user.email == user.email:
            raise ValidationError(REVIEW_CREATE_ERROR, HTTP_400_BAD_REQUEST) 
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Review:
        user: User = User.objects.get(email = validated_data['user'])
        send_to_user(user = user, message_type = REVIEW_CREATE_MESSAGE_TYPE)
        review: Review = Review.objects.create(email = self.context['request'].user.email, **validated_data)
        user: User = User.objects.get(email = validated_data['user'])
        for item in user.reviews.all():
            stars = item.stars
        user.raiting = stars / user.reviews.count()
        user.save()
        return review


class ReviewListSerializer(ModelSerializer):
    class Meta:
        model: Review = Review
        fields: Union[str, list[str]] = '__all__'

class ReviewUpdateSerializer(ModelSerializer):
    class Meta:
        model: Review = Review
        fields: Union[str, list[str]] = [
            'text', 
        ]