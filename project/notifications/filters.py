from typing import Union

from django_filters import (
    rest_framework as filters,
)
from notifications.models import Notification


class NotificationsFilterSet(filters.FilterSet):
    date_and_time = filters.DateFromToRangeFilter()

    class Meta:
        model: Notification = Notification
        fields: Union[str, list[str]] = ["type"]
