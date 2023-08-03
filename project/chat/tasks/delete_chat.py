from typing import Any, Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "delete_chat"
RESPONSE_TOPIC_NAME: str = "delete_chat_response"


def delete_chat_producer(
    *,
    chat_id: Optional[int] = None,
    event_id: Optional[int] = None,
    request_id: Optional[str] = None,
    request_user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "chat_id": chat_id,
        "request_user_id": request_user_id,
        "request_id": request_id,
        "event_id": event_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
