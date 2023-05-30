from typing import Type

from django.db.models import QuerySet
from hints.models import Hint
from hints.serializers import HintsListSerializer
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK


class HintsList(ListAPIView):
    """
    this endpoint allows the user
    to get a list of his current hints
    """

    serializer_class: Type[Serializer] = HintsListSerializer
    queryset: QuerySet[Hint] = Hint.get_all()

    def get_queryset(self) -> QuerySet[Hint]:
        return self.queryset.exclude(
            id__in=self.request.user.checked_hints.all().values("id")
        )


class CheckHints(GenericAPIView):
    """
    this endpoint allows the user to mark that he
    has already passed these hints and
    it can no longer be shown
    """
