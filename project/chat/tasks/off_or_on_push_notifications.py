from typing import Any, Union

from django.conf import settings
from kafka import KafkaConsumer
from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "off_or_on_push_notifications"
RESPONSE_TOPIC_NAME: str = "off_or_on_push_notifications_response"


def off_or_on_push_notifications_producer(
    *,
    data: dict[str, Union[str, int]],
    request_id: str,
    request_user_id: int,
) -> None:

    data_to_send: dict[str, Union[str, None, int]] = {
        "action": data["action"],
        "chat_id": data["chat_id"],
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def off_or_on_push_notifications_response_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
