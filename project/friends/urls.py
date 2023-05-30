from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from friends.views import (
    MyFriendsList,
    InviteUsersToFriends,
    InvitesToFriendsList,
    BulkAcceptOrDeclineInvitesToFriends,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/my/friends/list", MyFriendsList.as_view(), name="my-friends-list"),
    path(
        "client/my/invites/to/friends/list",
        InvitesToFriendsList.as_view(),
        name="my-invites-to-friends-list",
    ),
    path(
        "client/invite/users/to/friends",
        InviteUsersToFriends.as_view(),
        name="invite-users-to-friends",
    ),
    path(
        "client/accept/or/decline/invite/to/friends",
        BulkAcceptOrDeclineInvitesToFriends.as_view(),
        name="accept-decline-invite-to-friends",
    ),
]
