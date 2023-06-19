from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from project.chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_from_chat_message_to_the_ws
)

TOPIC_NAME: str = "get_chats_list"
RESPONSE_TOPIC_NAME: str = "get_chats_list_response"


@celery.task
def get_chats_list_producer(
    *,
    request_id: str,
    user_id: int,
    page: int = 1,
    offset: int = 10,
    search: Optional[str] = None
) -> str:

    if page is None:
        page = 1
    if offset is None:
        offset = 10

    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "user_id": user_id,
            "request_id": request_id,
            "page": page,
            "offset": offset,
            "search": search,
        },
    )
    producer.flush()


def get_chats_list_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_from_chat_message_to_the_ws(
            data=data.value
        )
