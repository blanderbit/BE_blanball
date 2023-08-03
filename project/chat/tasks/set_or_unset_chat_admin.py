from typing import Any, Union

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "set_or_unset_chat_admin"
RESPONSE_TOPIC_NAME: str = "set_or_unset_chat_admin_response"


def set_or_unset_chat_admin_producer(
    *,
    data: dict[str, Union[str, int]],
    request_id: str,
    request_user_id: int,
) -> None:

    data_to_send: dict[str, Union[str, None, int]] = {
        "user_id": data["user_id"],
        "action": data["action"],
        "chat_id": data["chat_id"],
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
