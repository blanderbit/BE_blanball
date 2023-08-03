from typing import Any

from notifications.tasks import (
    send_to_group_by_group_name,
)

WS_LAYERS: dict[str, str] = {"chat": "chat_user", "user": "user"}


def send_response_message_from_chat_to_the_ws(
    data: dict[str, Any], ws_layer: str = WS_LAYERS["chat"]
) -> None:

    main_data: dict[str, Any] = data["data"]
    message_type: str = data.pop("message_type")
    try:
        users = main_data.pop("users")
        for user in users:
            group_name = f"{ws_layer}_{user['user_id']}"
            send_message_to_group(group_name, message_type, data)
    except Exception:
        group_name = f"{ws_layer}_{data['request_data']['request_user_id']}"
        send_message_to_group(group_name, message_type, data)


def send_message_to_group(
    group_name: str, message_type: str, data: dict[str, Any]
) -> None:
    try:
        send_to_group_by_group_name(message_type, group_name, data)
    except Exception as _err:
        print(_err)
