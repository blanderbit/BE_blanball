from typing import Any

from authentication.models import User
from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from chat.utils import (
    send_response_from_chat_message_to_the_ws
)

TOPIC_NAME: str = "add_user_to_chat"
RESPONSE_TOPIC_NAME: str = "add_user_to_chat_response"


@celery.task
def add_user_to_chat_producer(*, user_id: int, event_id: int) -> None:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(TOPIC_NAME, value={"user_id": user_id, "event_id": event_id})
    producer.flush()


def add_user_to_chat_response_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_from_chat_message_to_the_ws(
            data=data.value
        )
