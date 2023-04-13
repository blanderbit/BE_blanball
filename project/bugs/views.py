from typing import Type

from api_keys.permissions import ApiKeyPermission
from bugs.constants.success import (
    BUG_REPORT_CREATED_SUCCESS,
)
from bugs.filters import (
    BUGS_LIST_ORDERING_FIELDS,
    BUGS_LIST_SEARCH_FIELDS,
    BugFilter,
)
from bugs.models import Bug
from bugs.openapi import bugs_list_query_params
from bugs.serializers import (
    BugsListSerializer,
    ChangeBugTypeSerializer,
    CreateBugSerializer,
    MyBugsListSerializer,
)
from bugs.services import (
    bulk_change_bugs_type,
    bulk_delete_bugs,
    create_bug,
)
from config.serializers import (
    BaseBulkSerializer,
)
from django.db.models import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from events.services import (
    skip_objects_from_response_by_id,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)


class CreateBug(GenericAPIView):
    """
    Create bug

    This endpoint allows the user who
    found the site to be not finalized to
    notify the administration about it
    """

    serializer_class: Type[Serializer] = CreateBugSerializer
    queryset: QuerySet[Bug] = Bug.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_bug(validated_data=serializer.validated_data, request_user=request.user)
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
    queryset: QuerySet[Bug] = Bug.get_all()
    permission_classes = [ApiKeyPermission | IsAuthenticated]
    filterset_class = BugFilter
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    ordering_fields = BUGS_LIST_ORDERING_FIELDS
    search_fields = BUGS_LIST_SEARCH_FIELDS

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
    permission_classes = [IsAuthenticated]

    @skip_objects_from_response_by_id
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class BulkDeleteBugs(GenericAPIView):
    """
    Delete bugs

    This endpoint allows the user to
    delete a certain number of bugs by ID.
    Example:
    {
        "ids": [
            1, 2, 3, 4, 5
        ]
    }
    If the user who sent the request has
    bugs under identifiers: 1,2,3,4,5
    then they will be read.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    permission_classes = [ApiKeyPermission]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = bulk_delete_bugs(ids=serializer.validated_data["ids"])
        return Response(data, HTTP_200_OK)


class ChangeBugType(GenericAPIView):
    """
    Change bug report type

    This endpoint allows admins to
    change the type of a bug report
    """

    serializer_class: Type[Serializer] = ChangeBugTypeSerializer
    permission_classes = [
        ApiKeyPermission,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = bulk_change_bugs_type(
            ids=serializer.validated_data["ids"], type=serializer.validated_data["type"]
        )
        return Response(data, HTTP_200_OK)
