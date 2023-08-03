from importlib import import_module

from chat.utils import (
    remove_from_end_of_string,
    send_response_message_from_chat_to_the_ws,
)
from django.conf import settings
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic


def read_topics_from_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        topics = [topic.strip() for topic in file.readlines()]
    return topics


def create_topics() -> list:
    admin_client: KafkaAdminClient = KafkaAdminClient(**settings.KAFKA_ADMIN_CONFIG)
    all_kafka_topics = read_topics_from_file("../kafka_topics_list.txt")
    existing_topics = admin_client.list_topics()
    consumer_topics = [
        NewTopic(name=topic, num_partitions=1, replication_factor=1)
        for topic in all_kafka_topics
        if (topic.endswith("response") or topic in existing_topics)
    ]
    admin_client.create_topics(new_topics=consumer_topics, validate_only=False)
    return admin_client.list_topics()


def default_consumer() -> None:
    consumer: KafkaConsumer = KafkaConsumer(**settings.KAFKA_CONSUMER_CONFIG)
    topics_to_subscribe = create_topics()

    consumer.subscribe(topics_to_subscribe)

    while True:
        raw_messages = consumer.poll(timeout_ms=100, max_records=200)
        for topic_partition, messages in raw_messages.items():
            for message in messages:
                topic_name: str = message.topic
                module_name: str = remove_from_end_of_string(topic_name, "_response")
                chat_task = import_module(f"chat.tasks.{module_name}")
                topic_function = getattr(chat_task, "process_response_data", None)
                if topic_function and callable(topic_function):
                    topic_function(data=message.value)
                else:
                    send_response_message_from_chat_to_the_ws(message.value)
