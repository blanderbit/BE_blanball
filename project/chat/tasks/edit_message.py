from typing import Any, Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "edit_message"
RESPONSE_TOPIC_NAME: str = "edit_message_response"


def edit_message_producer(
    *,
    message_id: int,
    request_id: Optional[str] = None,
    new_data: dict[str, Any],
    request_user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "message_id": message_id,
        "request_user_id": request_user_id,
        "request_id": request_id,
        "new_data": new_data,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
