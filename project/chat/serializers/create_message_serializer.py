
from typing import Union, Optional
from rest_framework.serializers import (
    CharField,
    IntegerField,
    Serializer,
    ValidationError,
)
from chat.utils import (
    generate_exception_fields_cant_be_provided_at_once,
    generate_exception_fields_must_be_provided
)
from chat.constants.errors import (
    YOU_CANT_SEND_MESSAGE_TO_YOURSELF
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


class CreateMessageSerializer(Serializer):

    text: str = CharField(max_length=500)
    chat_id: int = IntegerField(min_value=1, required=False)
    reply_to_message_id: int = IntegerField(min_value=1, required=False)
    user_id_for_request_chat: int = IntegerField(min_value=1, required=False)

    class Meta:
        fields: Union[str, list[str]] = [
            "text",
            "chat_id",
            "reply_to_message_id",
            "user_id_for_request_chat",
        ]

    def validate(self, attrs):
        chat_id: Optional[int] = attrs.get('chat_id')
        user_id_for_request_chat: Optional[int] = attrs.get('user_id_for_request_chat')
        reply_to_message_id: Optional[int] = attrs.get('reply_to_message_id')

        # if self.context["request"].user.id == user_id_for_request_chat:
        #     raise ValidationError(YOU_CANT_SEND_MESSAGE_TO_YOURSELF, HTTP_400_BAD_REQUEST)

        if not chat_id and not user_id_for_request_chat:
            raise ValidationError(generate_exception_fields_must_be_provided(
                ["chat_id", "user_id_for_request_chat"]
            ), HTTP_400_BAD_REQUEST)

        if chat_id and user_id_for_request_chat:
            raise ValidationError(generate_exception_fields_cant_be_provided_at_once
                                  (["chat_id", "user_id_for_request_chat"]
                                   ), HTTP_400_BAD_REQUEST)

        if reply_to_message_id and user_id_for_request_chat:
            raise ValidationError(generate_exception_fields_cant_be_provided_at_once(
                ["reply_to_message_id", "user_id_for_request_chat"]
            ), HTTP_400_BAD_REQUEST)

        return attrs
