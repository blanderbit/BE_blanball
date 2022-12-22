from typing import Union

from django_filters import (
    rest_framework as filters,
)
from bugs.models import Bug


class BugFilter(filters.FilterSet):
    time_created = filters.DateFromToRangeFilter()

    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = [
            "type"
        ]
