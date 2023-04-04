from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from events.views import (
    BulkAcceptOrDeclineInvitesToEvent,
    BulkAcceptOrDeclineRequestToParticipation,
    CreateEvent,
    DeleteEvents,
    EventsList,
    EventsRelevantList,
    FanJoinToEvent,
    FanLeaveFromEvent,
    GetEvent,
    InvitesToEventList,
    InviteUserToEvent,
    JoinToEvent,
    LeaveFromEvent,
    MyEventsList,
    MyFinishedEventsList,
    MyPinnedEventsCount,
    MyPlannedParticipantAndViewEventsList,
    MyTopicalEventsList,
    PinMyEvents,
    PlannedEventsList,
    PopularEventsList,
    RemoveUserFromEvent,
    RequestToParticipationsList,
    UnPinMyEvents,
    UpdateEvent,
    UserEventsRelevantList,
    UserParticipantEventsList,
    UserPlannedEventsList,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/event/create", CreateEvent.as_view(), name="event-create"),
    path("client/event/<int:pk>", GetEvent.as_view(), name="get-event"),
    path("client/event/update/<int:pk>", UpdateEvent.as_view(), name="update-event"),
    path("client/events/list", EventsList.as_view(), name="events-list"),
    path(
        "client/invites/to/events/list",
        InvitesToEventList.as_view(),
        name="invites-to-events-list",
    ),
    path("client/events/delete", DeleteEvents.as_view(), name="bulk-delete-events"),
    path("client/events/pin", PinMyEvents.as_view(), name="bulk-pin-events"),
    path("client/events/unpin", UnPinMyEvents.as_view(), name="bulk-unpin-events"),
    path("client/event/join", JoinToEvent.as_view(), name="join-to-event"),
    path(
        "client/remove/user/from/event",
        RemoveUserFromEvent.as_view(),
        name="remove-user-from-event",
    ),
    path("client/event/leave", LeaveFromEvent.as_view(), name="leave-from-event"),
    path(
        "client/fan/event/join",
        FanJoinToEvent.as_view(),
        name="spectator-join-to-event",
    ),
    path(
        "client/fan/event/leave",
        FanLeaveFromEvent.as_view(),
        name="spectator-leave-from-event",
    ),
    path("client/my/events/list", MyEventsList.as_view(), name="my-events-list"),
    path(
        "client/my/topical/events/list",
        MyTopicalEventsList.as_view(),
        name="my-topical-events-list",
    ),
    path(
        "client/my/finished/events/list",
        MyFinishedEventsList.as_view(),
        name="my-finished-events-list",
    ),
    path(
        "client/my/participant/events/list",
        UserParticipantEventsList.as_view(),
        name="user-participant-events-list",
    ),
    path(
        "client/relevant/events/list",
        EventsRelevantList.as_view(),
        name="relevant-event-list",
    ),
    path(
        "client/my/relevant/events/list",
        UserEventsRelevantList.as_view(),
        name="relevant-user-events-list",
    ),
    path(
        "client/user/planned/events/list/<int:pk>",
        UserPlannedEventsList.as_view(),
        name="user-planned-events-list",
    ),
    path(
        "client/my/planned/events/list",
        MyPlannedParticipantAndViewEventsList.as_view(),
        name="my-planned-events-list",
    ),
    path(
        "client/planned/events/list",
        PlannedEventsList.as_view(),
        name="planned-events-list",
    ),
    path(
        "client/popular/events/list",
        PopularEventsList.as_view(),
        name="popular-events-list",
    ),
    path(
        "client/invite/user/to/event",
        InviteUserToEvent.as_view(),
        name="invite-to-event",
    ),
    path(
        "client/requests/participations/list<int:pk>",
        RequestToParticipationsList.as_view(),
        name="request-participations-list",
    ),
    path(
        "client/accept/or/decline/participations",
        BulkAcceptOrDeclineRequestToParticipation.as_view(),
        name="accept-decline-participations",
    ),
    path(
        "client/accept/or/decline/invites/to/events",
        BulkAcceptOrDeclineInvitesToEvent.as_view(),
        name="accept-decline-invites-to-event",
    ),
    path(
        "client/my/pinned/events/count",
        MyPinnedEventsCount.as_view(),
        name="my-pinned-events-count",
    ),
]
