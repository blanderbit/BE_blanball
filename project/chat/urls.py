from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from chat.views import (
    CreateChat
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/chat/create", CreateChat.as_view(), name="chat-create"),
]
