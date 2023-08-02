from typing import Any, Optional


from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.helpers import default_producer, default_consumer

TOPIC_NAME: str = "get_chats_count"
RESPONSE_TOPIC_NAME: str = "get_chats_count_response"


def get_chats_count_producer(
    *,
    request_id: Optional[str] = None,
    request_user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def get_chats_count_response_consumer() -> None:

    consumer = default_consumer.delay(RESPONSE_TOPIC_NAME)

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
