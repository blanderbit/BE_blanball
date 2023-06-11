from datetime import date as datetimeDate
from datetime import datetime, timedelta
from typing import Union

from django.db.models import Q, QuerySet
from events.models import Event
from rest_framework.request import Request
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)
from scheduler.constants.errors import (
    SCHEDULED_EVENTS_DATE_INVALID,
)


def get_user_scheduled_events_data(
    data: dict[str, Union[str, int]], queryset: QuerySet[Event]
) -> dict[str, dict[str, int]]:

    start_date = data["start_date"]
    finish_date = data["finish_date"]
    user_id = data["user_id"]

    scheduled_events_data = {}

    current_date = start_date
    delta = timedelta(days=1)

    while current_date <= finish_date:
        events = queryset.filter(date_and_time__date=current_date)

        if len(events) > 0:

            user_scheduled_events_count = events.filter(
                Q(author__id=user_id)
                | Q(current_users__in=[user_id])
                | Q(current_fans__in=[user_id])
            ).count()

            if user_scheduled_events_count > 0:
                scheduled_events_data[str(current_date)] = {
                    "user_scheduled_events_count": user_scheduled_events_count,
                }

        current_date += delta

    return scheduled_events_data


def get_user_scheduled_events_on_specific_day(
    request: Request, queryest: QuerySet[Event]
) -> QuerySet[Event]:
    user_id = request.query_params.get("user_id")
    date = request.query_params.get("date")

    try:
        if not user_id:
            user_id = request.user.id
        if not date:
            date = datetimeDate.today()
        else:
            date = datetime.strptime(date, "%Y-%m-%d").date()

        return queryest.filter(
            Q(author__id=user_id)
            | Q(current_users__in=[user_id])
            | Q(current_fans__in=[user_id]),
            date_and_time__date=date,
        )

    except ValueError:
        raise ValidationError(SCHEDULED_EVENTS_DATE_INVALID, HTTP_400_BAD_REQUEST)
