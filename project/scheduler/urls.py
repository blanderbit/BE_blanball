from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

from scheduler.views import (
    UserScheduledEvents,
)


urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path(
        "client/user/scheduler/events",
        UserScheduledEvents.as_view(),
        name="user-scheduled-events"
    ),
]
