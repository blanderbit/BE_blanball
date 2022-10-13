from events.models import Event
from django_filters import rest_framework as filters

class EventDateTimeRangeFilter(filters.FilterSet):
    date_and_time = filters.DateFromToRangeFilter()

    class Meta:
        model = Event
        fields = ('date_and_time', )

# search_fields = ('event_data__name', 'small_disc', 'event_data__price', 'place', 'date_and_time', 'amount_members')