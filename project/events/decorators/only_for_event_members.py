from typing import Any

from events.models import Event
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.request import Request


def only_for_event_members(func):
    def wrap(self, request: Request, *agrs: Any, **kwargs: Any):
        try:
            event: Event = Event.objects.get(id=request.data["event"])
            if request.user in event.current_users.all():
                return func(self, request, *agrs, **kwargs)
            else:
                raise PermissionDenied()
        except Event.DoesNotExist:
            return func(self, request, *agrs, **kwargs)

    return wrap
