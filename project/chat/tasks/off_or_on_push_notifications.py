from typing import Union

from chat.helpers.default_producer import (
    default_producer,
)

TOPIC_NAME: str = "off_or_on_push_notifications"
RESPONSE_TOPIC_NAME: str = "off_or_on_push_notifications_response"


def off_or_on_push_notifications_producer(
    *,
    data: dict[str, Union[str, int]],
    request_id: str,
    request_user_id: int,
) -> None:

    data_to_send: dict[str, Union[str, None, int]] = {
        "action": data["action"],
        "chat_id": data["chat_id"],
        "request_user_id": request_user_id,
        "request_id": request_id,
    }

    default_producer.delay(topic_name=TOPIC_NAME, data=data_to_send)
