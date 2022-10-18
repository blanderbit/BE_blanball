from events.models import Event
from django_filters import rest_framework as filters

class EventDateTimeRangeFilter(filters.FilterSet):
    date_and_time = filters.DateFromToRangeFilter()

    class Meta:
        model: Event = Event
        fields = [
            'date_and_time',
            'type', 
            'need_ball', 
            'gender', 
            'status', 
            'duration',
        ]