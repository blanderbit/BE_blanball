from typing import (
    Any,
    Callable,
    Union,
)
from authentication.models import User
from django.db.models.query import QuerySet
from events.models import (
    Event,
)
from rest_framework_gis.filters import (
    DistanceToPointFilter,
)


def add_dist_filter_to_view(
    func: Callable[[..., ...], QuerySet[QuerySet[Union[User, Event]]]]
) -> Callable[[..., ...], QuerySet[QuerySet[Union[User, Event]]]]:
    def wrap(self) -> QuerySet[Union[User, Event]]:
        try:
            distance: int = self.request.query_params["dist"]
            if distance.isnumeric() or int(distance) > 0:
                self.filter_backends.append(DistanceToPointFilter)
                self.distance_filter_field = self.distance_ordering_filter_field
                return func(self)
        except Exception:
            return func(self)

    return wrap
