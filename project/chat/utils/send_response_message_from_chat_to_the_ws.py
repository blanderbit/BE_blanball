from typing import Any

from notifications.tasks import send_to_group_by_group_name


def send_response_message_from_chat_to_the_ws(data: dict[str, Any]) -> None:
    print(data, '------------------')
    main_data = data["data"]

    try:
        for user in main_data["users"]:
            group_name = f"user_{user['user_id']}"
            send_message_to_group(group_name, data["message_type"], data)
    except Exception:
        group_name = f"user_{data['request_user_id']}"
        send_message_to_group(group_name, data["message_type"], data)


def send_message_to_group(group_name: str, message_type: str, data: dict[str, Any]) -> None:
    print(data)
    try:
        send_to_group_by_group_name(group_name, message_type, data)
    except Exception:
        pass
