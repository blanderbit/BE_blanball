
from typing import Type
from hints.models import Hint
from hints.serializers import (
    HintsListSerializer
)

from django.db.models import (
    QuerySet,
    Q
)
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK


class HintsList(GenericAPIView):
    """
    this endpoint allows the user 
    to get a list of his current hints
    """

    serializer_class: Type[Serializer] = HintsListSerializer
    queryset: QuerySet[Hint] = Hint.get_all()

    def get(self, request: Request) -> Response:

        filtered_queryset: QuerySet[Hint] = self.queryset.exclude(
            id__in=request.user.checked_hints.all().values('id')
        )

        return Response(filtered_queryset, HTTP_200_OK)
