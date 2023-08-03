from typing import Any, Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "disable_chat"
RESPONSE_TOPIC_NAME: str = "disable_chat_response"


def disable_chat_producer(
    *,
    chat_id: Optional[int] = None,
    event_id: Optional[int] = None,
) -> str:

    data_to_send: dict[str, Any] = {
        "chat_id": chat_id,
        "event_id": event_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
