from typing import Any, Optional

from django.conf import settings
from kafka import KafkaConsumer
from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "get_chat_messages_list"
RESPONSE_TOPIC_NAME: str = "get_chat_messages_list_response"


def get_chat_messages_list_producer(
    *,
    request_id: str,
    user_id: int,
    chat_id: int,
    page: int = 1,
    offset: int = 10,
    search: Optional[str] = None
) -> str:

    if page is None:
        page = 1
    if offset is None:
        offset = 10

    data_to_send: dict[str, Any] = {
        "user_id": user_id,
        "chat_id": chat_id,
        "request_id": request_id,
        "page": page,
        "offset": offset,
        "search": search,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def get_chat_messages_list_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
