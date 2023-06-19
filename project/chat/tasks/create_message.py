from typing import Any
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)


TOPIC_NAME: str = "create_message"
RESPONSE_TOPIC_NAME: str = "create_message_response"


def create_message_producer(
    *,
    data: dict[str, Any],
    user_id: int,
    request_id: str,
) -> str:
    data_to_send: dict[str, Any] = {
        "text": data.get("text"),
        "user_id": user_id,
        "chat_id": data.get("chat_id"),
        "request_id": request_id,
        "reply_to_message_id": data.get("reply_to_message_id"),
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def create_message_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )
    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
