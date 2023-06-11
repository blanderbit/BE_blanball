from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from scheduler.views import (
    ListOfUserScheduledEventsOnSpecificDay,
    UserScheduledEvents,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path(
        "client/user/scheduler/events",
        UserScheduledEvents.as_view(),
        name="user-scheduled-events",
    ),
    path(
        "client/user/scheduler/events/on/specific/day",
        ListOfUserScheduledEventsOnSpecificDay.as_view(),
        name="user-scheduled-events-on-specific-day",
    ),
]
