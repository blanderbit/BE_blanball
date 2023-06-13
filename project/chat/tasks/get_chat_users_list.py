from config.celery import celery
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer

TOPIC_NAME: str = "get_chat_users_list"
RESPONSE_TOPIC_NAME: str = "get_chat_users_list_response"


@celery.task
def get_chat_users_list_producer(
    *,
    request_id: str,
    user_id: int,
    chat_id: int,
    page: int = 1,
    offset: int = 10,
) -> str:

    if page is None:
        page = 1
    if offset is None:
        offset = 10

    producer: KafkaProducer = KafkaProducer(**settings.KAFKA_PRODUCER_CONFIG)
    producer.send(
        TOPIC_NAME,
        value={
            "user_id": user_id,
            "chat_id": chat_id,
            "request_id": request_id,
            "page": page,
            "offset": offset,
        },
    )
    producer.flush()


def get_chat_users_list_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        print(data.value)
