import json
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    TypeVar,
)

from authentication.models import User
from notifications.constants.notification_types import (
    CHANGE_MAINTENANCE_NOTIFICATION_TYPE,
    NOTIFICATIONS_BULK_DELETE_NOTIFICATION_TYPE,
    NOTIFICATIONS_BULK_READ_NOTIFICATION_TYPE,
)
from notifications.models import Notification
from notifications.tasks import (
    send,
    send_to_general_layer,
)

bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])


def update_maintenance(*, data: dict[str, str]) -> None:

    with open("./config/config.json", "r") as f:
        json_data = json.load(f)
        json_data["isMaintenance"] = data["isMaintenance"]

    with open("./config/config.json", "w") as f:
        f.write(json.dumps(json_data))

        send_to_general_layer(
            message_type=CHANGE_MAINTENANCE_NOTIFICATION_TYPE,
            data={
                "maintenance": {
                    "type": data["isMaintenance"],
                }
            },
        )


def send_message_after_bulk_method(message_type: str) -> ...:
    def wrap(
        func: Callable[[Any, Any], bulk]
    ) -> Callable[[Any, Any], dict[str, list[int]]]:
        def callable(*args: Any, **kwargs: Any) -> dict[str, list[int]]:
            objects_ids: list[int] = list(func(*args, **kwargs))
            if len(objects_ids) > 0:
                try:
                    send(
                        user=kwargs["user"],
                        data={
                            "type": "kafka.message",
                            "message": {
                                "message_type": message_type,
                                "objects": objects_ids,
                            },
                        },
                    )
                except IndexError:
                    pass
            return {"success": objects_ids}

        return callable

    return wrap


@send_message_after_bulk_method(NOTIFICATIONS_BULK_DELETE_NOTIFICATION_TYPE)
def bulk_delete_notifications(*, ids: dict[str, int], user: User) -> bulk:
    for notification in ids:
        try:
            notify = Notification.objects.get(id=notification)
            if notify.user == user:
                notify.delete()
                yield notification
        except Notification.DoesNotExist:
            pass


@send_message_after_bulk_method(NOTIFICATIONS_BULK_READ_NOTIFICATION_TYPE)
def bulk_read_notifications(*, ids: dict[str, int], user: User) -> bulk:
    for notification in ids:
        try:
            notify = Notification.objects.get(id=notification)
            if notify.type != "Read" and notify.user == user:
                notify.type = "Read"
                notify.save()
                yield notification
        except Notification.DoesNotExist:
            pass
