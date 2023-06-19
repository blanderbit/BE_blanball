from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from chat.utils import (
    send_response_from_chat_message_to_the_ws
)


TOPIC_NAME: str = "create_message"
RESPONSE_TOPIC_NAME: str = "create_message_response"


@celery.task
def create_message_producer(
    *,
    data: dict[str, Any],
    user_id: int,
    request_id: str,
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "text": data.get("text"),
            "user_id": user_id,
            "chat_id": data.get("chat_id"),
            "request_id": request_id,
            "reply_to_message_id": data.get("reply_to_message_id"),
        },
    )
    producer.flush()


def create_message_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )
    for data in consumer:
        send_response_from_chat_message_to_the_ws(
            data=data.value
        )
