from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import (
    send_to_group_by_group_name,
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
        try:
            all_recieved_data: dict[str, Any] = data.value["data"]
            users: list[dict[str, int]] = all_recieved_data["users"]
            message_type: str = data.value["message_type"]
            for user in users:
                send_to_group_by_group_name(
                    group_name=f"user_{user['user_id']}",
                    message_type=message_type,
                    data={
                        "chat_id": all_recieved_data["chat_id"],
                        "message": all_recieved_data["message_data"],
                        "not_read_messages_count": all_recieved_data["not_read_messages_count"]
                    },
                )
        except Exception:
            pass
