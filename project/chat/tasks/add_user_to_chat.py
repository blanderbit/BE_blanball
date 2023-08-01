from typing import Any
from django.conf import settings
from kafka import KafkaConsumer
from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.serializers import (
    ChatUserSerializer
)
from authentication.models import User
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "add_user_to_chat"
RESPONSE_TOPIC_NAME: str = "add_user_to_chat_response"


def add_user_to_chat_producer(*, user_id: int, event_id: int) -> None:

    data_to_send: dict[str, int] = {
        "user_id": user_id,
        "event_id": event_id
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def process_response_data(data: dict[str, Any]) -> None:

    if isinstance(data["data"], dict):
        new_user_id = data["data"].pop("new_user_id")
        new_user = User.objects.get(id=new_user_id)
        new_user_data = ChatUserSerializer(new_user).data
        data["data"]["new_user_data"] = new_user_data
        data["data"]["service_message"].pop("sender_id")
        data["data"]["service_message"]["sender"] = new_user_data

    send_response_message_from_chat_to_the_ws(
        data=data
    )


def add_user_to_chat_response_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        process_response_data(data.value)
