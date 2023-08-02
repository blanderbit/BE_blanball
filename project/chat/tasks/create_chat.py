from typing import Optional

from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.helpers import default_producer, default_consumer

TOPIC_NAME: str = "create_chat"
RESPONSE_TOPIC_NAME: str = "create_chat_response"


def create_chat_producer(*, 
      data: dict[str, str],
      author_id: int, 
      type: Optional[str] = None, 
      request_id: str
) -> str:
    data["request_user_id"] = author_id
    data["request_id"] = request_id
    if type:
        data["type"] = type

    default_producer.delay(topic_name=TOPIC_NAME, data=data)


def create_chat_response_consumer() -> None:

    consumer = default_consumer.delay(RESPONSE_TOPIC_NAME, send_response_message_from_chat_to_the_ws)

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
