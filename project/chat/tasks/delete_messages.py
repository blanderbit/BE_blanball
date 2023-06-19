from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import send_to_chat_layer

TOPIC_NAME: str = "delete_messages"
RESPONSE_TOPIC_NAME: str = "delete_messages_response"


@celery.task
def delete_messages_producer(
    *, message_ids: int, request_id: Optional[str] = None, user_id: int
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "message_ids": message_ids,
            "user_id": user_id,
            "request_id": request_id,
        },
    )
    producer.flush()


def delete_messages_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        all_recieved_data: dict[str, Any] = data.value["data"]
        users: list[dict[str, int]] = data.value["data"]["users"]
        message_type: str = data.value["message_type"]
        for user in users:
            send_to_chat_layer(
                user_id=user["user_id"],
                message_type=message_type,
                data={
                    "chat_id": all_recieved_data["chat_id"],
                    "message": all_recieved_data["message_data"],
                },
            )
