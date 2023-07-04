
from typing import Union

from authentication.models import (
    User,
)
from rest_framework.serializers import (
    Serializer,
    BooleanField,
)
from chat.serializers.chat_user_serializer import (
    ChatUserSerializer
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
            "author",
            "disabled",
            "removed",
            "admin",
            "chat_deleted",
            "user_data"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users_list = self.context.get("users_list")
        if users_list:
            for user in users_list:
                serializer = ChatUserSerializer(user)
                user_data = serializer.data
                data['user_data'] = user_data
        return data
