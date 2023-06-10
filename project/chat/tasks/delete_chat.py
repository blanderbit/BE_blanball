from typing import Optional

from kafka import KafkaProducer, KafkaConsumer
from django.conf import settings
from config.celery import celery

TOPIC_NAME: str = 'delete_chat'
RESPONSE_TOPIC_NAME: str = 'delete_chat_response'


@celery.task
def delete_chat_producer(*, 
        chat_id: int, 
        request_id: str, 
        user_id: int
    ) -> str:
    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(TOPIC_NAME, value={
        "chat_id": chat_id,
        "user_id": user_id,
        "request_int": request_id
    })
    producer.flush()


def delete_chat_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG)

    for data in consumer:
        print(data.value)
