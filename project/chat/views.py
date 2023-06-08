from typing import Type
from chat.tasks import (
    create_chat_producer,
)
from chat.serializers import (
    CreatePersonalChatSerializer,
    CreateGroupChatSerializer,
)
from utils.generate_unique_request_id import (
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

    """

    serializer_class: Type[Serializer] = CreateGroupChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_request_id = generate_unique_request_id()
        create_chat_producer.delay(
            data=serializer.validated_data,
            author_id=request.user.id,
            type="Group",
            request_id=unique_request_id
        )
        return Response({"request_id": unique_request_id}, HTTP_201_CREATED)
