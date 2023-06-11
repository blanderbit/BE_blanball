from typing import Union

from chat.views import (
    CreateGroupChat,
    CreateMessage,
    DeleteChat,
    EditChat,
    RemoveUserFromChat,
    GetChatsList,
    EditChatMessage
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path(
        "client/group/chat/create", CreateGroupChat.as_view(), name="group-chat-create"
    ),
    path("client/create/message", CreateMessage.as_view(), name="create-message"),
    path(
        "client/remove/user/from/chat",
        RemoveUserFromChat.as_view(),
        name="remove-user-from-chat",
    ),
    path("client/delete/chat", DeleteChat.as_view(), name="remove-user-from-chat"),
    path("client/edit/chat", EditChat.as_view(), name="edit-chat"),
    path("client/get/chats/list", GetChatsList.as_view(), name="get-chat-lists"),
    path("client/edit/chat/message", EditChatMessage.as_view(), name="edit-chat-message")
]
