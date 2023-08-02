from typing import Optional, Union, Any


from chat.utils.send_response_message_from_chat_to_the_ws import (
    send_response_message_from_chat_to_the_ws
)
from chat.helpers import default_producer, default_consumer
from authentication.models import (
    User
)
from chat.serializers import (
    GetChatsListSerializer
)

TOPIC_NAME: str = "get_chats_list"
RESPONSE_TOPIC_NAME: str = "get_chats_list_response"


def get_chats_list_producer(
    *,
    request_id: str,
    request_user_id: int,
    page: int = 1,
    offset: int = 10,
    search: Optional[str] = None,
    chats_type: Optional[str] = None
) -> str:

    if page is None:
        page = 1
    if offset is None:
        offset = 10

    data_to_send: dict[str, Union[str, int]] = {
        "request_user_id": request_user_id,
        "request_id": request_id,
        "page": page,
        "offset": offset,
        "search": search,
        "chats_type": chats_type
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)


def process_response_data(data: dict[str, Any]) -> None:
    results_chats_list = None

    if isinstance(data["data"], dict):
        results_chats_list = data["data"].get("results")

    if results_chats_list:
        user_ids = [item['last_message'].get('sender_id') for item in results_chats_list]
        users = User.objects.filter(id__in=user_ids)
        serializer = GetChatsListSerializer(
            results_chats_list,
            many=True,
            context={'users_list': [user for user in users]}
        )

        data["data"]["results"] = [dict(result) for result in serializer.data]

    send_response_message_from_chat_to_the_ws(data=data)


def get_chats_list_response_consumer() -> None:

    consumer = default_consumer.delay(RESPONSE_TOPIC_NAME)

    for data in consumer:
        process_response_data(data.value)
