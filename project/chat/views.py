from typing import Type
from chat.tasks import (
    create_chat_producer,
    create_message_producer
)
from chat.serializers import (
    CreatePersonalChatSerializer,
    CreateGroupChatSerializer,
    CreateMessageSerializer,
)
from utils import (
    generate_unique_request_id
)

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)


class CreateGroupChat(GenericAPIView):

    """
    Create group chat

    This endpoint allows the user to create 
    a group chat and invite other users there.
    """

    serializer_class: Type[Serializer] = CreateGroupChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()
        create_chat_producer.delay(
            data=serializer.validated_data,
            author_id=request.user.id,
            type="Group",
            request_id=unique_request_id
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)


class CreateMessage(GenericAPIView):

    """
    Create message

    This endpoint allows the user to create 
    a group chat and invite other users there.
    """

    serializer_class: Type[Serializer] = CreateMessageSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id: str = generate_unique_request_id()
        create_message_producer.delay(
            data=serializer.validated_data,
            author_id=request.user.id,
            request_id=unique_request_id
        )
        return Response({"request_id": unique_request_id}, HTTP_200_OK)
