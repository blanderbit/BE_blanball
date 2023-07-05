from typing import Union
from rest_framework.serializers import (
    ChoiceField,
    IntegerField,
    ListField,
    Serializer,
)

READ_OR_UNREAD_MESSAGE_CHOICES: tuple[tuple[str]] = (("read", "read"), ("unread", "unread"))


class ReadOrUnreadMessagesSerializer(Serializer):
    message_ids: list[int] = ListField(child=IntegerField(min_value=0))
    action: str = ChoiceField(choices=READ_OR_UNREAD_MESSAGE_CHOICES)

    class Meta:
        fields: Union[str, list[str]] = ["message_ids", "action"]
