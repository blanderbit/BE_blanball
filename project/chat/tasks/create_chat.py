from typing import Optional
from django.conf import settings
from kafka import KafkaConsumer
from chat.utils import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)

TOPIC_NAME: str = "create_chat"
RESPONSE_TOPIC_NAME: str = "create_chat_response"


def create_chat_producer(*, 
      data: dict[str, str],
      author_id: int, 
      type: Optional[str] = None, 
      request_id: str
) -> str:
    data["request_user_id"] = author_id
    data["request_id"] = request_id
    if type:
        data["type"] = type

    default_producer.delay(topic_name=TOPIC_NAME, data=data)


def create_chat_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        send_response_message_from_chat_to_the_ws(
            data=data.value
        )
