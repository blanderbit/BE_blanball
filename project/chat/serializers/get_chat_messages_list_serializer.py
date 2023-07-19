
from typing import Union
from rest_framework.serializers import (
    Serializer,
    IntegerField,
    CharField,
    ListField,
    BooleanField
)
from chat.serializers.chat_user_serializer import (
    ChatUserSerializer
)


class GetChatMessagesListSerializer(Serializer):
    id = IntegerField()
    text = CharField()
    edited = BooleanField()
    service = BooleanField()
    type = CharField()
    time_created = CharField()
    reply_to = IntegerField()
    readed_by = ListField()
    sender = ChatUserSerializer(read_only=True)

    class Meta:
        fields: Union[str, list[str]] = [
            "id",
            "sender",
            "text",
            "time_created",
            "edited",
            "readed_by",
            "reply_to",
            "type",
            "service"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users_list = self.context.get("users_list")
        if users_list:
            user_id = instance['sender_id']
            for user in users_list:
                print(user)
                if user.id == user_id:
                    serializer = ChatUserSerializer(user)
                    user_data = serializer.data
                    data['sender'] = user_data
                    break
        return data
