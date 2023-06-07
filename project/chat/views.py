from typing import Type
from chat.tasks import (
    create_chat_producer,
)
from chat.serializers import (
    CreateChatSerializer
)

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)


class CreateChat(GenericAPIView):

    """
    Create chat

    """

    serializer_class: Type[Serializer] = CreateChatSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_chat_producer.delay(
            data=serializer.validated_data, 
            author_id=request.user.id
        )
        return Response(HTTP_201_CREATED)
