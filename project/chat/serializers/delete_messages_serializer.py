from typing import Union

from rest_framework.serializers import (
    IntegerField,
    ListField,
    Serializer,
)


class DeleteMessagesSerializer(Serializer):
    message_ids: list[int] = ListField(child=IntegerField(min_value=0))

    class Meta:
        fields: Union[str, list[str]] = ["message_ids"]
