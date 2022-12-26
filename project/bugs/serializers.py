from typing import Union

from authentication.serializers import (
    ReviewAuthorSerializer,
)
from bugs.models import (
    Bug,
    BugImage,
)
from rest_framework import serializers


class CreateBugSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(), required=False
    )
    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = [
            "title",
            "description",
            "images",
        ]

class BugsListImagesNameSerializer(serializers.ModelSerializer):

    class Meta:
        model: BugImage = BugImage
        fields: Union[str, list[str]] = [
            "image_url"
        ]


class BugsListSerializer(serializers.ModelSerializer):

    author = ReviewAuthorSerializer()
    images = BugsListImagesNameSerializer(many=True)

    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = "__all__"


class MyBugsListSerializer(serializers.ModelSerializer):
    class Meta:
        model: Bug = Bug
        exclude: list[str] = ["author"]


class BulkDeleteBugsSerializer(serializers.Serializer):
    ids: list[int] = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        fields: Union[str, list[str]] = [
            "ids",
        ]
