from typing import Union

from rest_framework.serializers import (
    CharField,
    IntegerField,
    Serializer,
)


class NewChatDataSerializer(Serializer):
    name: str = CharField(max_length=355, required=False)

    class Meta:
        fields: Union[str, list[str]] = ["name"]


class EditChatSerializer(Serializer):

    chat_id: int = IntegerField(min_value=1)
    new_data: dict[str, str] = NewChatDataSerializer()

    class Meta:
        fields: Union[str, list[str]] = ["chat_id", "new_data"]
