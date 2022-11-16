import json
from typing import (
    Any,
    Generator,
    Optional,
    TypeVar,
    Callable,
)

from asgiref.sync import async_to_sync
from authentication.models import User
from channels.layers import get_channel_layer
from django.db.models.query import QuerySet
from notifications.constants.notification_types import (
    CHANGE_MAINTENANCE_NOTIFICATION_TYPE,
    NOTIFICATIONS_BULK_READ_NOTIFICATION_TYPE,
    NOTIFICATIONS_BULK_DELETE_NOTIFICATION_TYPE,
)
from notifications.models import Notification
from notifications.tasks import send

bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])


def update_maintenance(*, data: dict[str, str]) -> None:

    with open("./config/config.json", "r") as f:
        json_data = json.load(f)
        json_data["isMaintenance"] = data["isMaintenance"]

    with open("./config/config.json", "w") as f:
        f.write(json.dumps(json_data))

        async_to_sync(get_channel_layer().group_send)(
            "general",
            {
                "type": "general.message",
                "message": {
                    "message_type": CHANGE_MAINTENANCE_NOTIFICATION_TYPE,
                    "data": {
                        "maintenance": {
                            "type": data["isMaintenance"],
                        }
                    },
                },
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
def bulk_delete_notifications(
    *, data: dict[str, Any], queryset: QuerySet[Notification], user: User
) -> bulk:
    for notification in data:
        try:
            notify = queryset.get(id=notification)
            if notify.user == user:
                notify.delete()
                yield notification
        except Notification.DoesNotExist:
            pass


@send_message_after_bulk_method(NOTIFICATIONS_BULK_READ_NOTIFICATION_TYPE)
def bulk_read_notifications(
    *, data: dict[str, Any], queryset: QuerySet[Notification], user: User
) -> bulk:
    for notification in data:
        try:
            notify = queryset.get(id=notification)
            if notify.type != "Read" and notify.user == user:
                notify.type = "Read"
                notify.save()
                yield notification
        except Notification.DoesNotExist:
            pass
