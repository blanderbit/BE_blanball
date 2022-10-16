from events.models import Event
from django_filters import rest_framework as filters

from typing import Union

class EventDateTimeRangeFilter(filters.FilterSet):
    date_and_time = filters.DateFromToRangeFilter()

    class Meta:
        model = Event
        fields: Union[str, list[str]] = [
            'date_and_time', 
        ]