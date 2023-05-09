
from typing import Union
from datetime import (
    timedelta
)
from events.models import (
    Event
)
from django.db.models import (
    QuerySet,
    Q
)


def get_user_scheduled_events_data(
    data: dict[str, Union[str, int]],
    queryset: QuerySet[Event]
) -> dict[str, dict[str, int]]:

    start_date = data['start_date']
    finish_date = data['finish_date']
    user_id = data['user_id']

    scheduled_events_data = {}

    current_date = start_date
    delta = timedelta(days=1)

    while current_date <= finish_date:
        events = queryset.filter(
            date_and_time__date=current_date
        )

        if len(events) > 0:

            user_scheduled_events_count = events.filter(
                author__id=user_id |
                Q(current_users=user_id) |
                Q(current_fans=user_id)
            ).count()

            if user_scheduled_events_count > 0:
                scheduled_events_data[str(current_date)] = {
                    'user_scheduled_events_count': user_scheduled_events_count,
                }

        current_date += delta

    return scheduled_events_data
