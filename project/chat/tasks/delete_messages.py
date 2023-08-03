from typing import Any, Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "delete_messages"
RESPONSE_TOPIC_NAME: str = "delete_messages_response"


def delete_messages_producer(
    *,
    message_ids: int,
    request_id: Optional[str] = None,
    request_user_id: int,
    chat_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "message_ids": message_ids,
        "request_user_id": request_user_id,
        "request_id": request_id,
        "chat_id": chat_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
