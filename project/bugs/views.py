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
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from bugs.serializers import (
    CreateBugSerializer,
    BugsListSerializer,
    MyBugsListSerializer,
    BulkDeleteBugsSerializer,
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
from bugs.openapi import  (
    bugs_list_query_params,
)
from bugs.services import (
    bulk_delete_bugs
)
from events.services import (
    skip_objects_from_response_by_id,
)
from django.db.models import QuerySet
from django.utils.decorators import (
    method_decorator,
)

class CreateBug(GenericAPIView):
    """
    Create bug

    This endpoint allows the user who 
    found the site to be not finalized to 
    notify the administration about it
    """
    serializer_class: Type[Serializer] = CreateBugSerializer
    parser_classes = [MultiPartParser]
    queryset: QuerySet[Bug] = Bug.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        Bug.objects.create(author=request.user, **serializer.validated_data)
        return Response(BUG_REPORT_CREATED_SUCCESS, HTTP_201_CREATED)

@method_decorator(
    swagger_auto_schema(manual_parameters=bugs_list_query_params),
    name="get",
)
class BugsList(ListAPIView):
    """
    Bugs list

    This endpoint allows the user to get 
    a list of all the bugs (open and already closed),
    as well as filter them
    """

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

    @skip_objects_from_response_by_id
    def get_queryset(self):
        return self.queryset

class MyBugs(BugsList):
    """
    My bugs list

    This endpoint allows the user to get 
    a list of all the bugs that he opened 
    (open and closed), as well as filter them
    """
    serializer_class: Type[Serializer] = MyBugsListSerializer

    @skip_objects_from_response_by_id
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

class BulkDeleteBugs(GenericAPIView):
    """
    Bulk delete bugs

    """
    serializer_class: Type[Serializer] = BulkDeleteBugsSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = bulk_delete_bugs(
            ids=serializer.validated_data["ids"], user=request.user
        )
        return Response(data, HTTP_200_OK)