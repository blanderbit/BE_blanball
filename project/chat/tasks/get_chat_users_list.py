from typing import Union, Any

from django.conf import settings
from kafka import KafkaConsumer
from authentication.models import User
from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.tasks.default_producer import (
    default_producer
)
from chat.serializers import (
    GetChatUsersListSerializer
)

TOPIC_NAME: str = "get_chat_users_list"
RESPONSE_TOPIC_NAME: str = "get_chat_users_list_response"


def get_chat_users_list_producer(
    *,
    request_id: str,
    request_user_id: int,
    chat_id: int,
    page: int = 1,
    offset: int = 10,
) -> str:

    if page is None:
        page = 1
    if offset is None:
        offset = 10

    data_to_send: dict[str, Union[str, int]] = {
        "request_user_id": request_user_id,
        "chat_id": chat_id,
        "request_id": request_id,
        "page": page,
        "offset": offset,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def process_response_data(data: dict[str, Any]) -> None:
    results_users_list = None

    if isinstance(data["data"], dict):
        results_users_list = data["data"].get("results")

    if results_users_list:
        user_ids = [item['user_id'] for item in results_users_list]
        users = User.objects.filter(id__in=user_ids)
        users_list = {user for user in users}

        serializer = GetChatUsersListSerializer(
            results_users_list,
            many=True,
            context={'users_list': users_list}
        )

        data["data"]["results"] = [dict(result) for result in serializer.data]

    send_response_message_from_chat_to_the_ws(data=data)


def get_chat_users_list_response_consumer() -> None:

    consumer: KafkaConsumer = KafkaConsumer(
        RESPONSE_TOPIC_NAME, **settings.KAFKA_CONSUMER_CONFIG
    )

    for data in consumer:
        process_response_data(data.value)