from kafka import KafkaProducer
from django.conf import settings
from config.celery import celery


def base_producer(message) -> None:
    producer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send('my_topic', value=message)