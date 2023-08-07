from typing import Any, Type

from chat.openapi import (
    chat_users_list_query_params,
    chats_list_query_params,
)
from chat.serializers import (
    CreateGroupChatSerializer,
    CreateMessageSerializer,
    DeleteChatSerializer,
    DeleteMessagesSerializer,
    EditChatMessageSerializer,
    EditChatSerializer,
    OffOrOnChatPushNotificationsSerializer,
    ReadOrUnreadMessagesSerializer,
    RemoveUserFromChatSerializer,
    SetOrUnsetChatAdminSerializer,
)
from chat.tasks import (
    create_chat_producer,
    create_message_producer,
    delete_chat_producer,
    delete_messages_producer,
    edit_chat_producer,
    edit_message_producer,
    get_chat_detail_data_producer,
    get_chat_messages_list_producer,
    get_chat_users_list_producer,
    get_chats_count_producer,
    get_chats_list_producer,
    off_or_on_push_notifications_producer,
    read_or_unread_messages_producer,
    remove_user_from_chat_producer,
    set_or_unset_chat_admin_producer,
)
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from utils import generate_unique_request_id


class CreateGroupChat(GenericAPIView):

    """
    Create group chat

    This endpoint allows the
    user to create a group chat.
    """

    serializer_class: Type[Serializer] = CreateGroupChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()
        create_chat_producer(
            data=serializer.validated_data,
            author_id=request.user.id,
            type="Group",
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class CreateMessage(GenericAPIView):

    """
    Create message

    This endpoint allows the user to create a
    message in the chat if he is a member of it.
    """

    serializer_class: Type[Serializer] = CreateMessageSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()
        create_message_producer(
            data=serializer.validated_data,
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class RemoveUserFromChat(GenericAPIView):

    """
    Remove user from chat

    This endpoint allows the user to remove other
    users from the chat if he is the author or admin.
    """

    serializer_class: Type[Serializer] = RemoveUserFromChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        remove_user_from_chat_producer(
            user_id=serializer.validated_data["user_id"],
            chat_id=serializer.validated_data["chat_id"],
            request_id=unique_request_id,
            request_user_id=request.user.id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class DeleteChat(GenericAPIView):
    """
    Delete chat

    This endpoint allows the user to delete
    the chat if he is its author or admin.
    """

    serializer_class: Type[Serializer] = DeleteChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        delete_chat_producer(
            chat_id=serializer.validated_data["chat_id"],
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class EditChat(GenericAPIView):
    """
    Edit chat

    This endpoint allows the user
    to edit the chat data.
    """

    serializer_class: Type[Serializer] = EditChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        edit_chat_producer(
            chat_id=serializer.validated_data["chat_id"],
            request_user_id=request.user.id,
            request_id=unique_request_id,
            new_data=serializer.validated_data["new_data"],
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


@method_decorator(
    swagger_auto_schema(manual_parameters=chats_list_query_params),
    name="get",
)
class GetChatsList(GenericAPIView):
    """
    Get my chats list

    This endpoint allows the user to get a
    list of chats in which he is a member.
    """

    def get(self, request: Request) -> Response:
        unique_request_id: str = generate_unique_request_id()

        query: dict[str, Any] = request.query_params

        get_chats_list_producer(
            request_user_id=request.user.id,
            request_id=unique_request_id,
            offset=query.get("offset"),
            page=query.get("page"),
            search=query.get("search"),
            chats_type=query.get("chats_type"),
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


@method_decorator(
    swagger_auto_schema(manual_parameters=chats_list_query_params),
    name="get",
)
class GetChatMessagesList(GenericAPIView):
    """
    Get messages list of certain chat

    This endpoint allows the user to get a
    list of messages in the chat they are members of.
    """

    def get(self, request: Request, chat_id: int) -> Response:
        unique_request_id: str = generate_unique_request_id()

        query: dict[str, Any] = request.query_params

        get_chat_messages_list_producer(
            request_user_id=request.user.id,
            chat_id=chat_id,
            request_id=unique_request_id,
            offset=query.get("offset"),
            page=query.get("page"),
            search=query.get("search"),
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


@method_decorator(
    swagger_auto_schema(manual_parameters=chat_users_list_query_params),
    name="get",
)
class GetChatUsersList(GenericAPIView):
    """
    Get users list of certain chat

    This endpoint allows the user to get a
    list of users in the chat they are members of.
    """

    def get(self, request: Request, chat_id: int) -> Response:
        unique_request_id: str = generate_unique_request_id()

        query: dict[str, Any] = request.query_params

        get_chat_users_list_producer(
            request_user_id=request.user.id,
            chat_id=chat_id,
            request_id=unique_request_id,
            offset=query.get("offset"),
            page=query.get("page"),
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class EditChatMessage(GenericAPIView):
    """
    Edit chat message

    This endpoint allows the user to edit a
    previously sent chat message.
    """

    serializer_class: Type[Serializer] = EditChatMessageSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        edit_message_producer(
            message_id=serializer.validated_data["message_id"],
            request_user_id=request.user.id,
            request_id=unique_request_id,
            new_data=serializer.validated_data["new_data"],
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class ReadOrUnreadMessages(GenericAPIView):
    """
    Read or Unread messages

    This endpoint allows the user to mark
    messages as read or, conversely, as unread.
    """

    serializer_class: Type[Serializer] = ReadOrUnreadMessagesSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        read_or_unread_messages_producer(
            message_ids=serializer.validated_data["message_ids"],
            request_user_id=request.user.id,
            request_id=unique_request_id,
            action=serializer.validated_data["action"],
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class DeleteChatMessages(GenericAPIView):
    """
    Delete chat messages

    This endpoint allows the user to delete
    messages in a chat that he previously sent.
    """

    serializer_class: Type[Serializer] = DeleteMessagesSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        delete_messages_producer(
            message_ids=serializer.validated_data["message_ids"],
            chat_id=serializer.validated_data["chat_id"],
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class SetOrUnsetChatAdmin(GenericAPIView):
    """
    Set chat admin

    This endpoint allows the user to delete
    messages in a chat that he previously sent.
    """

    serializer_class: Type[Serializer] = SetOrUnsetChatAdminSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        set_or_unset_chat_admin_producer(
            data=serializer.validated_data,
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class OffOrOnChatPushNotifications(GenericAPIView):
    """
    Off or on chat push notifications

    This endpoint allows the user to delete
    messages in a chat that he previously sent.
    """

    serializer_class: Type[Serializer] = OffOrOnChatPushNotificationsSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()

        off_or_on_push_notifications_producer(
            data=serializer.validated_data,
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class GetChatDetailData(GenericAPIView):
    """
    Chat detail data

    This endpoint allows the user to delete
    messages in a chat that he previously sent.
    """

    def get(self, request: Request, chat_id: int) -> Response:
        unique_request_id: str = generate_unique_request_id()

        get_chat_detail_data_producer(
            chat_id=chat_id,
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class GetMyChatsCount(GenericAPIView):
    """
    Get all my chats count

    This endpoint allows the user to delete
    messages in a chat that he previously sent.
    """

    def get(self, request: Request) -> Response:
        unique_request_id: str = generate_unique_request_id()

        get_chats_count_producer(
            request_user_id=request.user.id,
            request_id=unique_request_id,
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)
