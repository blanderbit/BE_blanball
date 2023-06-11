from typing import (
    Any,
    Callable,
)
from config.exceptions import _404
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.request import Request
from rest_framework.response import Response


def only_author(Object):
    def wrap(
        func: Callable[[Request, int, ...], Response]
    ) -> Callable[[Request, int, ...], Response]:
        def called(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Any:
            try:
                if self.request.user.id == Object.objects.get(id=pk).author.id:
                    return func(self, request, pk, *args, **kwargs)
                raise PermissionDenied()
            except Object.DoesNotExist:
                raise _404(object=Object)

        return called

    return wrap
