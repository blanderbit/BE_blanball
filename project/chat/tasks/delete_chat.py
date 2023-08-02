from typing import Any, Optional


from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.helpers import default_producer, default_consumer

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


def delete_chat_response_consumer() -> None:

    consumer = default_consumer.delay(RESPONSE_TOPIC_NAME)

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
