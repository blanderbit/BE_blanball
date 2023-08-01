from typing import Union

from chat.views import (
    CreateGroupChat,
    CreateMessage,
    DeleteChat,
    DeleteChatMessages,
    EditChat,
    EditChatMessage,
    GetChatMessagesList,
    GetChatsList,
    ReadOrUnreadMessages,
    RemoveUserFromChat,
    GetChatUsersList,
    SetOrUnsetChatAdmin,
    GetChatDetailData,
    OffOrOnChatPushNotifications,
    GetMyChatsCount,
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
        "client/off/or/on/chat/push/notifications",
        OffOrOnChatPushNotifications.as_view(),
        name="off-or-on-chat-push-notifications"
    ),
    path(
        "client/remove/user/from/chat",
        RemoveUserFromChat.as_view(),
        name="remove-user-from-chat",
    ),
    path("client/delete/chat", DeleteChat.as_view(), name="remove-user-from-chat"),
    path("client/edit/chat", EditChat.as_view(), name="edit-chat"),
    path("client/get/chats/list", GetChatsList.as_view(), name="get-chat-lists"),
    path(
        "client/get/chat/detail/data/<int:chat_id>",
        GetChatDetailData.as_view(),
        name="get-chat-detail-data"
    ),
    path(
        "client/get/all/my/chats/count",
        GetMyChatsCount.as_view(),
        name="get-all-my-chats-count"
    ),
    path(
        "client/edit/chat/message", EditChatMessage.as_view(), name="edit-chat-message"
    ),
    path(
        "client/chat/messages/list/<int:chat_id>",
        GetChatMessagesList.as_view(),
        name="chat-messages-list",
    ),
    path(
        "client/chat/users/list/<int:chat_id>",
        GetChatUsersList.as_view(),
        name="chat-users-list",
    ),
    path(
        "client/read/or/unread/messages",
        ReadOrUnreadMessages.as_view(),
        name="read-or-unread-messages",
    ),
    path(
        "client/delete/chat/messages",
        DeleteChatMessages.as_view(),
        name="delete-chat-messages",
    ),
    path(
        "client/chat/set/or/unset/admin",
        SetOrUnsetChatAdmin.as_view(),
        name="chat-set-or-unset-admin",
    ),
]
