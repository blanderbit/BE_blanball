from typing import Union

from bugs.models import Bug
from django_filters import (
    rest_framework as filters,
)


class BugFilter(filters.FilterSet):
    time_created = filters.DateFromToRangeFilter()

    class Meta:
        model: Bug = Bug
        fields: Union[str, list[str]] = ["type"]
