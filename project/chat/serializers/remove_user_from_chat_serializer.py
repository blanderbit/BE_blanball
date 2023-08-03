from typing import Union

from rest_framework.serializers import (
    IntegerField,
    Serializer,
)


class RemoveUserFromChatSerializer(Serializer):

    chat_id: int = IntegerField(min_value=1)
    user_id: int = IntegerField(min_value=1)

    class Meta:
        fields: Union[str, list[str]] = ["chat_id", "user_id"]
