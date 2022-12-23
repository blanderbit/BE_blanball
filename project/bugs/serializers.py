from typing import Union

from authentication.serializers import (
    ReviewAuthorSerializer,
)
from bugs.models import Bug
from rest_framework import serializers


class CreateBugSerializer(serializers.ModelSerializer):
    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = [
            "title",
            "description",
            "image",
        ]


class BugsListSerializer(serializers.ModelSerializer):

    author = ReviewAuthorSerializer()

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
