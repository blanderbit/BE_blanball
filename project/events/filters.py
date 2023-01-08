from typing import Union

from django_filters import (
    rest_framework as filters,
)
from events.models import Event

EVENTS_LIST_ORDERING_FIELDS: list[str] = [
    "id",
    "-id",
]
EVENTS_LIST_SEARCH_FIELDS: list[str] = [
    "name",
    "price",
    "amount_members",
]
EVENTS_RELEVANT_LIST_SEARCH_FIELDS: list[str] = [
    "name",
]
EVENTS_LIST_DISTANCE_ORDERING_FIELD: str = "coordinates"


class EventDateTimeRangeFilter(filters.FilterSet):
    date_and_time = filters.DateFromToRangeFilter()

    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "date_and_time",
            "type",
            "need_ball",
            "gender",
            "status",
            "duration",
        ]
