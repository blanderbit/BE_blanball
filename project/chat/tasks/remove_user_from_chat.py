from typing import Optional, Union

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "remove_user_from_chat"
RESPONSE_TOPIC_NAME: str = "remove_user_from_chat_response"


def remove_user_from_chat_producer(
    *,
    user_id: int,
    request_id: Optional[str] = None,
    event_id: Optional[int] = None,
    chat_id: Optional[int] = None,
    request_user_id: Optional[int] = None
) -> None:

    data_to_send: dict[str, Union[str, None, int]] = {
        "user_id": user_id,
        "event_id": event_id,
        "chat_id": chat_id,
        "request_id": request_id,
        "request_user_id": request_user_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
