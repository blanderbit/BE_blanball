
from typing import Union

from rest_framework.serializers import (
    BooleanField,
    CharField,
    IntegerField,
    Serializer,
)
from chat.serializers import (
    ChatUserSerializer
)


class ChatLastMessageSerializer(Serializer):
    id = IntegerField()
    text = CharField()
    time_created = CharField()
    type = CharField()
    service = BooleanField()
    sender = ChatUserSerializer(read_only=True)

    class Meta:
        fields: Union[str, list[str]] = [
            "id",
            "text",
            "time_created",
            "type",
            "sender",
            "service",
        ]


class GetChatsListSerializer(Serializer):
    id = IntegerField()
    name = CharField()
    image = CharField()
    disabled = BooleanField()
    type = CharField()
    unread_messages_count = IntegerField()
    is_group = BooleanField()
    last_message = ChatLastMessageSerializer()

    class Meta:
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "type",
            "image",
            "disabled",
            "last_message",
            "unread_messages_count",
            "is_group",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users_list = self.context.get("users_list")
        if users_list:
            user_id = instance['last_message'].get('sender_id')
            for user in users_list:
                if user.id == user_id:
                    serializer = ChatUserSerializer(user)
                    user_data = serializer.data
                    data['last_message']['sender'] = user_data
                    break
        return data
