from typing import Type

from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from bugs.serializers import (
    CreateBugSerializer,
    BugsListSerializer,
)
from bugs.models import (
    Bug,
)
from bugs.constants.success import (
    BUG_REPORT_CREATED_SUCCESS,
)
from bugs.filters import (
    BugFilter,
)
from django.db.models import QuerySet

class CreateBug(GenericAPIView):
    serializer_class: Type[Serializer] = CreateBugSerializer
    parser_classes = [MultiPartParser]
    queryset: QuerySet[Bug] = Bug.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        Bug.objects.create(author=request.user, **serializer.validated_data)
        return Response(BUG_REPORT_CREATED_SUCCESS, HTTP_201_CREATED)


class BugsList(ListAPIView):
    serializer_class: Type[Serializer] = BugsListSerializer
    queryset: QuerySet[Bug] = Bug.objects.all().order_by('-id')
    filterset_class = BugFilter
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    ordering_fields: list[str] = [
        "id",
    ]
    search_fields: list[str] = ["title"]