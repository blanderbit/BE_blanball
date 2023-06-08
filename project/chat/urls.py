from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from chat.views import (
    CreateGroupChat
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/group/chat/create", CreateGroupChat.as_view(), name="group-chat-create"),
]
