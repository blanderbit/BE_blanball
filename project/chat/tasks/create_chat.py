from typing import Optional, Any

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import (
    send_to_chat_layer
)

TOPIC_NAME: str = "create_chat"
RESPONSE_TOPIC_NAME: str = "create_chat_response"


@celery.task
def create_chat_producer(
    *, data: dict[str, str], author_id: int, type: Optional[str] = None, request_id: str
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    data["author"] = author_id
    data["request_id"] = request_id
    if type:
        data["type"] = type
    producer.send(TOPIC_NAME, value=data)
    producer.flush()


def create_chat_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        try:
            all_recieved_data: dict[str, Any] = data.value["data"]
            users: list[dict[str, Any]] = all_recieved_data["users"]
            message_type: str = data.value["message_type"]
            for user in users:
                send_to_chat_layer(
                    user_id=user["user_id"],
                    message_type=message_type,
                    data={
                        "chat_data": all_recieved_data["chat_data"]
                    }
                )
        except Exception:
            pass
