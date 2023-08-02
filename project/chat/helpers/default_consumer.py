from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer


@celery.task
def default_consumer(topic_name: str, callback) -> str:
    consumer: KafkaConsumer = KafkaConsumer(
        topic_name, **settings.KAFKA_CONSUMER_CONFIG
    )
    callback()
