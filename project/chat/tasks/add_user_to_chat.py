from typing import Any

from authentication.models import User
from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer
from notifications.tasks import send_to_chat_layer

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

        try:
            all_recieved_data: dict[str, Any] = data.value["data"]
            message_type: str = data.value["message_type"]
            users: list[dict[str, Any]] = data.value["data"]["users"]
            new_user: User = User.objects.get(id=all_recieved_data["new_user"])
            for user in users:
                send_to_chat_layer(
                    user_id=user,
                    message_type=message_type,
                    data={
                        "chat_id": all_recieved_data["chat_id"],
                        "new_user": {
                            "id": new_user.id,
                            "name": new_user.profile.name,
                            "last_name": new_user.profile.last_name,
                            "avatar": new_user.profile.avatar_url,
                        },
                    },
                )
        except Exception:
            pass
