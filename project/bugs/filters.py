from typing import Union

from bugs.models import Bug
from django_filters import (
    rest_framework as filters,
)
BUGS_LIST_ORDERING_FIELDS: list[str] = [
    "id", 
    "-id",
]
BUGS_LIST_SEARCH_FIELDS: list[str] = [
    "title",
]
BUGS_LIST_CHOICE_FILTER_FIELDS: list[str] = [
    "type", 
]



class BugFilter(filters.FilterSet):
    time_created = filters.DateFromToRangeFilter()

    class Meta:
        model: Bug = Bug
        fields = BUGS_LIST_CHOICE_FILTER_FIELDS
