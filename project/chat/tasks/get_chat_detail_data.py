from typing import Any, Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "get_chat_detail_data"
RESPONSE_TOPIC_NAME: str = "get_chat_detail_data_response"


def get_chat_detail_data_producer(
    *, chat_id: int, request_id: Optional[str] = None, request_user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "chat_id": chat_id,
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
