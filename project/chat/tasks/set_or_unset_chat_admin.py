from typing import Any, Optional, Union

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import send_to_chat_layer

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
                        "new_admin_id": all_recieved_data["new_admin_id"]
                    },
                )
        except Exception:
            pass
