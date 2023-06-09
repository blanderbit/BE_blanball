from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from chat.views import (
    CreateGroupChat,
    CreateMessage,
    RemoveUserFromChat
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/group/chat/create", CreateGroupChat.as_view(), name="group-chat-create"),
    path("client/create/message", CreateMessage.as_view(), name="create-message"),
    path("client/remove/user/from/chat", RemoveUserFromChat.as_view(), name="remove-user-from-chat"),
]
