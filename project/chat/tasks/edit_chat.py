from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from project.chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_from_chat_message_to_the_ws
)

TOPIC_NAME: str = "edit_chat"
RESPONSE_TOPIC_NAME: str = "edit_chat_response"


@celery.task
def edit_chat_producer(
    *,
    chat_id: Optional[int] = None,
    event_id: Optional[int] = None,
    request_id: Optional[str] = None,
    new_data: dict[str, Any],
    user_id: int
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "chat_id": chat_id,
            "user_id": user_id,
            "request_id": request_id,
            "event_id": event_id,
            "new_data": new_data,
        },
    )
    producer.flush()


def edit_chat_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_from_chat_message_to_the_ws(
            data=data.value
        )
