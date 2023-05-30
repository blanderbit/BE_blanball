# ==============================================================================
# users_list.py file which includes all controllers responsible for working
# with users lists, search, filtering, sorting, selection and relevant search
# ==============================================================================
from typing import Any, Type

from api_keys.permissions import ApiKeyPermission
from authentication.filters import (
    USERS_LIST_DISTANCE_ORDERING_FIELD,
    USERS_LIST_ORDERING_FIELDS,
    USERS_LIST_SEARCH_FIELDS,
    USERS_RELEVANT_LIST_SEARCH_FIELDS,
    RankedFuzzySearchFilter,
    UserAgeRangeFilter,
)
from authentication.models import User
from authentication.openapi import (
    users_list_query_params,
    users_relevant_list_query_params,
)
from authentication.serializers import (
    UsersListDetailSerializer,
    UsersListSerializer,
)
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from utils import (
    skip_objects_from_response_by_id,
    add_dist_filter_to_view,
    paginate_by_offset,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.serializers import Serializer
from rest_framework_gis.filters import (
    DistanceToPointOrderingFilter,
)


@method_decorator(
    swagger_auto_schema(manual_parameters=users_list_query_params, tags=["users"]),
    name="get",
)
@paginate_by_offset
class UsersList(ListAPIView):
    """
    List of users

    This class makes it possible to
    get a list of all users of the application.
    """

    serializer_class: Type[Serializer] = UsersListSerializer
    queryset: QuerySet[User] = User.get_all()
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
        DistanceToPointOrderingFilter,
    ]
    filterset_class = UserAgeRangeFilter
    ordering_fields = USERS_LIST_ORDERING_FIELDS
    search_fields = USERS_LIST_SEARCH_FIELDS
    distance_ordering_filter_field = USERS_LIST_DISTANCE_ORDERING_FIELD
    distance_filter_convert_meters: bool = True
    permission_classes = [ApiKeyPermission | IsAuthenticated]

    @skip_objects_from_response_by_id
    @add_dist_filter_to_view
    def get_queryset(self) -> QuerySet[User]:
        return self.queryset.filter(role="User")


class UsersDetailList(UsersList):
    """
    List of users for admins

    This class makes it possible to
    get a list of all users of the application.
    """

    permission_classes = [ApiKeyPermission]
    serializer_class: Type[Serializer] = UsersListDetailSerializer


@method_decorator(
    swagger_auto_schema(
        manual_parameters=users_relevant_list_query_params, tags=["users"]
    ),
    name="get",
)
class UsersRelevantList(ListAPIView):
    """
    Relevant user search

    This class makes it possible to get the 5 most
    relevant users for a search query.
    """

    filter_backends = [
        RankedFuzzySearchFilter,
    ]
    permission_classes = [ApiKeyPermission | IsAuthenticated]
    serializer_class: Type[Serializer] = UsersListSerializer
    queryset: QuerySet[User] = User.get_all()
    search_fields = USERS_RELEVANT_LIST_SEARCH_FIELDS

    def get_queryset(self) -> QuerySet[User]:
        return UsersList.get_queryset(self)
