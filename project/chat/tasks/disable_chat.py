from typing import Optional, Any

from django.conf import settings
from kafka import KafkaConsumer
from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "disable_chat"
RESPONSE_TOPIC_NAME: str = "disable_chat_response"


def disable_chat_producer(
    *,
    chat_id: Optional[int] = None,
    event_id: Optional[int] = None,
) -> str:

    data_to_send: dict[str, Any] = {
        "chat_id": chat_id,
        "event_id": event_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def disable_chat_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
