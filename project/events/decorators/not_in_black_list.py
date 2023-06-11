from typing import (
    Any,
    Callable,
)
from config.exceptions import _404
from events.models import (
    Event,
)
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.request import Request
from rest_framework.response import Response


def not_in_black_list(
    func: Callable[[Request, int, ...], Response]
) -> Callable[[Request, int, ...], Response]:
    def wrap(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Any:
        try:
            if request.user in Event.objects.get(id=pk).black_list.all():
                raise PermissionDenied()
            return func(self, request, pk, *args, **kwargs)
        except Event.DoesNotExist:
            raise _404(object=Event)

    return wrap
