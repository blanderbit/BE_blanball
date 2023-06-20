from typing import Any, Optional
from django.conf import settings
from kafka import KafkaConsumer
from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)
from chat.serializers import ChatUserSerializer
from authentication.models import User


TOPIC_NAME: str = "create_message"
RESPONSE_TOPIC_NAME: str = "create_message_response"


def create_message_producer(
    *,
    data: dict[str, Any],
    request_user_id: int,
    request_id: str,
) -> str:
    data_to_send: dict[str, Any] = {
        "text": data.get("text"),
        "request_user_id": request_user_id,
        "chat_id": data.get("chat_id"),
        "request_id": request_id,
        "reply_to_message_id": data.get("reply_to_message_id"),
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def process_response_data(data: dict[str, Any]) -> None:
    if isinstance(data["data"], dict):
        message_data = data["data"]["message_data"]
        sender_id = message_data.pop("sender_id", None)

        if sender_id is not None:
            try:
                sender_user = User.objects.get(id=sender_id)
                serializer = ChatUserSerializer(sender_user)
                message_data["sender"] = dict(serializer.data)
            except User.DoesNotExist:
                pass

    send_response_message_from_chat_to_the_ws(data=data)


def create_message_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )
    for data in consumer:
        process_response_data(data.value)
