from typing import (
    Any,
    Callable,
)

from django.db.models import Q
from django.db.models.query import QuerySet


def skip_objects_from_response_by_id(
    func: Callable[[..., ...], QuerySet[Any]]
) -> Callable[[..., ...], QuerySet[Any]]:
    def wrap(self, *args: Any, **kwargs: Any) -> Any:
        try:
            self.queryset = self.queryset.filter(
                ~Q(id__in=list(self.request.query_params["skipids"].split(",")))
            )
            return func(self, *args, **kwargs)
        except (KeyError, ValueError):
            pass
        finally:
            return func(self, *args, **kwargs)

    return wrap
