from typing import Any, Optional, Union


from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.helpers import default_producer, default_consumer

TOPIC_NAME: str = "read_or_unread_messages"
RESPONSE_TOPIC_NAME: str = "read_or_unread_messages_response"


def read_or_unread_messages_producer(
    *, message_ids: int, request_id: str, action: str, request_user_id: int
) -> str:

    data_to_send: dict[str, Union[str, int, list[Optional[int]]]] = {
        "message_ids": message_ids,
        "request_user_id": request_user_id,
        "request_id": request_id,
        "action": action,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def read_or_unread_messages_response_consumer() -> None:

    consumer = default_consumer.delay(RESPONSE_TOPIC_NAME)

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
