from typing import Any, Optional

from django.conf import settings
from kafka import KafkaConsumer
from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "delete_messages"
RESPONSE_TOPIC_NAME: str = "delete_messages_response"


def delete_messages_producer(
    *, message_ids: int, request_id: Optional[str] = None, request_user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "message_ids": message_ids,
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def delete_messages_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )