from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from friends.views import (
    MyFriendsList
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/my/friends/list", MyFriendsList.as_view(), name="my-friends-list"),
]
