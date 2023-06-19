from django.conf import settings
from kafka import KafkaConsumer
from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
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


def add_user_to_chat_response_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
