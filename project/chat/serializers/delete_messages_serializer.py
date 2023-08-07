from typing import Union

from rest_framework.serializers import (
    IntegerField,
    ListField,
    Serializer,
)


class DeleteMessagesSerializer(Serializer):
    chat_id: int = IntegerField(min_value=1)
    message_ids: list[int] = ListField(child=IntegerField(min_value=0))

    class Meta:
        fields: Union[str, list[str]] = ["chat_id", "message_ids"]
