from typing import Any, Union
from collections import OrderedDict

from authentication.models import User
from authentication.serializers import FriendUserSerializer
from config.exceptions import _404
from config.serializers import (
    BaseBulkSerializer,
)
from friends.models import (
    Friend,
    InviteToFriends,
)
from rest_framework.serializers import (
    BooleanField,
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


class MyFriendsListSerializer(ModelSerializer):
    friend = FriendUserSerializer()

    class Meta:
        model: Friend = Friend
        fields: Union[str, list[str]] = ["id", "friend", "created_at"]


class InvitesToFriendsListSerializer(ModelSerializer):
    sender = FriendUserSerializer()

    class Meta:
        model: InviteToFriends = InviteToFriends
        fields: Union[str, list[str]] = [
            "id",
            "time_created",
            "sender",
        ]


class BulkAcceptOrDeclineInvitionsToFriendsSerializer(BaseBulkSerializer):
    type: bool = BooleanField()

    class Meta:
        fields: Union[str, list[str]] = [
            "type",
        ]
