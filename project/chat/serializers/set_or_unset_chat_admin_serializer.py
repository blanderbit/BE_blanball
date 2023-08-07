from typing import Union

from rest_framework.serializers import (
    ChoiceField,
    IntegerField,
    Serializer,
)

SER_OR_UNSET_ADMIM_CHOICES: tuple[tuple[str]] = (("set", "set"), ("unset", "unset"))


class SetOrUnsetChatAdminSerializer(Serializer):
    user_id: int = IntegerField(min_value=1)
    chat_id: int = IntegerField(min_value=1)
    action: str = ChoiceField(choices=SER_OR_UNSET_ADMIM_CHOICES)

    class Meta:
        fields: Union[str, list[str]] = ["user_id", "chat_id", "action"]
