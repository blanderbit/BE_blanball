from typing import Any

from config.celery import celery
from django.conf import settings
from kafka import KafkaProducer

producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)

@celery.task
def default_producer(*, topic_name: str, data: dict[str, Any]) -> str:
    producer.send(topic_name, value=data)
    producer.flush()
