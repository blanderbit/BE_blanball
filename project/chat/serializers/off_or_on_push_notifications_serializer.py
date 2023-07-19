from typing import Union
from rest_framework.serializers import (
    ChoiceField,
    IntegerField,
    Serializer,
)

OFF_OR_ON_CHAT_PUSH_NOTIFICATIONS_CHOICES: tuple[tuple[str]] = (("on", "on"), ("off", "off"))


class OffOrOnChatPushNotificationsSerializer(Serializer):
    chat_id: int = IntegerField(min_value=1)
    action: str = ChoiceField(choices=OFF_OR_ON_CHAT_PUSH_NOTIFICATIONS_CHOICES)

    class Meta:
        fields: Union[str, list[str]] = ["chat_id", "action"]
