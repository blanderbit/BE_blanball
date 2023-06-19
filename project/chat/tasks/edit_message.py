from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer
from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "edit_message"
RESPONSE_TOPIC_NAME: str = "edit_message_response"


def edit_message_producer(
    *,
    message_id: int,
    request_id: Optional[str] = None,
    new_data: dict[str, Any],
    user_id: int
) -> str:

    data_to_send: dict[str, Any] = {
        "message_id": message_id,
        "user_id": user_id,
        "request_id": request_id,
        "new_data": new_data,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def edit_message_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
