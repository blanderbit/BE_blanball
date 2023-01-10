from typing import Union

from authentication.serializers import (
    ReviewAuthorSerializer,
)
from bugs.models import Bug, BugImage
from rest_framework.serializers import (
    ImageField,
    ListField,
    ModelSerializer,
)


class CreateBugSerializer(ModelSerializer):

    images = ListField(child=ImageField(), required=False)

    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = [
            "title",
            "description",
            "images",
        ]


class BugsListImagesNameSerializer(ModelSerializer):
    class Meta:
        model: BugImage = BugImage
        fields: Union[str, list[str]] = ["image_url"]


class BugsListSerializer(ModelSerializer):

    author = ReviewAuthorSerializer()
    images = BugsListImagesNameSerializer(many=True)

    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = "__all__"


class MyBugsListSerializer(ModelSerializer):
    class Meta:
        model: Bug = Bug
        exclude: list[str] = ["author"]
