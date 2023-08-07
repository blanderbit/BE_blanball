from typing import Union

from authentication.models import User
from chat.serializers.chat_user_serializer import (
    ChatUserSerializer,
)
from rest_framework.serializers import (
    BooleanField,
    Serializer,
)


class GetChatUsersListSerializer(Serializer):
    author: bool = BooleanField()
    disabled: bool = BooleanField()
    removed: bool = BooleanField()
    admin: bool = BooleanField()
    chat_deleted: bool = BooleanField()
    user_data: User = ChatUserSerializer(read_only=True)

    class Meta:
        fields: Union[str, list[str]] = [
            "id",
            "author",
            "disabled",
            "removed",
            "admin",
            "chat_deleted",
            "user_data",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users_list = self.context.get("users_list")
        if users_list:
            user_id = instance["user_id"]
            for user in users_list:
                if user.id == user_id:
                    serializer = ChatUserSerializer(user)
                    user_data = serializer.data
                    data["id"] = user.id
                    data["user_data"] = user_data
                    break
        return data
