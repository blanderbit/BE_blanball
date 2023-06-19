from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import send_to_chat_layer

TOPIC_NAME: str = "remove_user_from_chat"
RESPONSE_TOPIC_NAME: str = "remove_user_from_chat_response"


@celery.task
def remove_user_from_chat_producer(
    *,
    user_id: int,
    request_id: str,
    event_id: Optional[int] = None,
    chat_id: Optional[int] = None,
    sender_user_id: Optional[int] = None
) -> None:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "user_id": user_id,
            "sender_user_id": sender_user_id,
            "event_id": event_id,
            "chat_id": chat_id,
            "request_id": request_id,
        },
    )
    producer.flush()


def remove_user_from_chat_response_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:

        try:
            all_recieved_data: dict[str, Any] = data.value["data"]
            message_type: str = data.value["message_type"]
            users: list[dict[str, int]] = data.value["data"]["users"]
            for user in users:
                send_to_chat_layer(
                    user_id=user,
                    message_type=message_type,
                    data={
                        "chat_id": all_recieved_data["chat_id"],
                        "removed_user_id": all_recieved_data["removed_user_id"]
                    },
                )
        except Exception:
            pass
