from typing import Any, Union

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from project.chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_from_chat_message_to_the_ws
)

TOPIC_NAME: str = "set_or_unset_chat_admin_admin"
RESPONSE_TOPIC_NAME: str = "set_or_unset_chat_admin_response"


@celery.task
def set_or_unset_chat_admin_producer(
    *,
    data: dict[str, Union[str, int]],
    request_id: str,
    author_id: int,
) -> None:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "user_id": data["user_id"],
            "action": data["action"],
            "chat_id": data["chat_id"],
            "author_id": author_id,
            "request_id": request_id,
        },
    )
    producer.flush()


def set_or_unset_chat_admin_response_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_from_chat_message_to_the_ws(
            data=data.value
        )
