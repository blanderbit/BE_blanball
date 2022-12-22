from typing import Union

from rest_framework import serializers
from bugs.models import Bug
from authentication.serializers import ReviewAuthorSerializer



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