from typing import Any, Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "get_chats_count"
RESPONSE_TOPIC_NAME: str = "get_chats_count_response"


def get_chats_count_producer(
    *, request_id: Optional[str] = None, request_user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
