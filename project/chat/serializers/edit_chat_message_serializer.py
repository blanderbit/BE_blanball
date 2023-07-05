from typing import Union

from rest_framework.serializers import (
    CharField,
    IntegerField,
    Serializer,
)


class NewChatMessageDataSerializer(Serializer):
    text: str = CharField(max_length=500, required=False)

    class Meta:
        fields: Union[str, list[str]] = ["text"]


class EditChatMessageSerializer(Serializer):

    message_id: int = IntegerField(min_value=1)
    new_data: dict[str, str] = NewChatMessageDataSerializer()

    class Meta:
        fields: Union[str, list[str]] = ["message_id", "new_data"]
