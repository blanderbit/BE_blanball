from typing import Optional, Any

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import (
    send_to_chat_layer
)

TOPIC_NAME: str = "disable_chat"
RESPONSE_TOPIC_NAME: str = "disable_chat_response"


@celery.task
def disable_chat_producer(
    *,
    chat_id: Optional[int] = None,
    event_id: Optional[int] = None,
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "chat_id": chat_id,
            "event_id": event_id,
        },
    )
    producer.flush()


def disable_chat_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        try:
            all_recieved_data: dict[str, Any] = data.value["data"]
            users: list[dict[str, int]] = data.value["data"]["users"]
            message_type: str = data.value["message_type"]
            for user in users:
                send_to_chat_layer(
                    user_id=user["user_id"],
                    message_type=message_type,
                    data={
                        "chat_id": all_recieved_data["chat_id"],
                    },
                )
        except Exception:
            pass
