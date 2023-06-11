from typing import Optional

from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer

TOPIC_NAME: str = "create_message"
RESPONSE_TOPIC_NAME: str = "create_message_response"


@celery.task
def create_message_producer(*,
                            text: str,
                            user_id: int,
                            chat_id: int,
                            request_id: str
                            ) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(TOPIC_NAME, value={
        "text": text,
        "user_id": user_id,
        "chat_id": chat_id,
        "request_id": request_id
    })
    producer.flush()


def create_message_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        print(data.value)
