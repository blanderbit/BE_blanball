from typing import Optional

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "create_chat"
RESPONSE_TOPIC_NAME: str = "create_chat_response"


def create_chat_producer(
    *, data: dict[str, str], author_id: int, type: Optional[str] = None, request_id: str
) -> str:
    data["request_user_id"] = author_id
    data["request_id"] = request_id
    if type:
        data["type"] = type

    default_producer.delay(topic_name=TOPIC_NAME, data=data)
