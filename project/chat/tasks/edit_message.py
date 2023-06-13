from typing import Any, Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import send_to_chat_layer

TOPIC_NAME: str = "edit_message"
RESPONSE_TOPIC_NAME: str = "edit_message_response"


@celery.task
def edit_message_producer(
    *,
    message_id: int,
    request_id: Optional[str] = None,
    new_data: dict[str, Any],
    user_id: int
) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "message_id": message_id,
            "user_id": user_id,
            "request_id": request_id,
            "new_data": new_data,
        },
    )
    producer.flush()


def edit_message_response_consumer() -> None:

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
                        "chat_id": all_recieved_data["chat_id"],
                        "messsage_new_data": all_recieved_data["new_data"],
                    },
                )
        except Exception:
            pass
