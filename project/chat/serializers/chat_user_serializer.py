from typing import Union

from authentication.models import (
    User,
    Profile
)
from authentication.serializers import (
    CommonUserProfileSerializer
)
from rest_framework.serializers import (
    ModelSerializer,
)


class ChatUserProfileSerializer(CommonUserProfileSerializer):
    def to_representation(self, value):
        return dict(super().to_representation(value))


class ChatUserSerializer(ModelSerializer):
    profile: Profile = ChatUserProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "role",
            "is_online",
            "profile",
        ]

    def to_representation(self, value):
        return dict(super().to_representation(value))
