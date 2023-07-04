
from typing import Union
from rest_framework.serializers import (
    CharField,
    IntegerField,
    Serializer,
)


class CreateMessageSerializer(Serializer):

    text: str = CharField(max_length=500)
    chat_id: int = IntegerField(min_value=1)
    reply_to_message_id: int = IntegerField(min_value=1, required=False)

    class Meta:
        fields: Union[str, list[str]] = [
            "text",
            "chat_id",
            "reply_to_message_id"
        ]
