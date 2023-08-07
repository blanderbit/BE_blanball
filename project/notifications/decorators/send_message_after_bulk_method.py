from typing import Any, Callable

from notifications.tasks import send


def send_message_after_bulk_method(message_type: str) -> ...:
    def wrap(
        func: Callable[[Any, Any], Any]
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
