from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from project.chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_from_chat_message_to_the_ws
)

TOPIC_NAME: str = "read_or_unread_messages"
RESPONSE_TOPIC_NAME: str = "read_or_unread_messages_response"


@celery.task
def read_or_unread_messages_producer(
    *, message_ids: int, request_id: Optional[str] = None, action: str, user_id: int
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "message_ids": message_ids,
            "user_id": user_id,
            "request_id": request_id,
            "action": action,
        },
    )
    producer.flush()


def read_or_unread_messages_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_from_chat_message_to_the_ws(
            data=data.value
        )
