from typing import Any, Type, final

from authentication.models import User
from config.exceptions import _404
from config.pagination import paginate_by_offset
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from friends.models import (
    Friend,
    InviteToFriends
)
from friends.serializers import (
    MyFriendsListSerializer,
    InvitesToFriendsListSerializer,
)
from friends.filters import (
    MY_FRIENDS_LIST_ORDERING_FIELDS,
    MY_FRIENDS_LIST_SEARCH_FIELDS,
    MyFriendsListFilterSet
)
from friends.openapi import (
    my_friends_list_query_params
)
from config.openapi import (
    offset_query,
    skip_param_query,
)
from events.services import (
    skip_objects_from_response_by_id,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK


@method_decorator(
    swagger_auto_schema(manual_parameters=my_friends_list_query_params),
    name="get",
)
@paginate_by_offset
class MyFriendsList(ListAPIView):
    """
    List of my friends

    This endpoint allows the user to receive,
    filter and sort the complete list of her friends.
    """

    serializer_class: Type[Serializer] = MyFriendsListSerializer
    search_fields = MY_FRIENDS_LIST_SEARCH_FIELDS
    ordering_fields = MY_FRIENDS_LIST_ORDERING_FIELDS
    filterset_class = MyFriendsListFilterSet
    queryset: QuerySet[Friend] = Friend.get_all()
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Friend]:
        return self.queryset.filter(user_id=self.request.user.id)
    

@method_decorator(
    swagger_auto_schema(
        manual_parameters=[skip_param_query, offset_query],
        tags=["invites-to-friends"]
    ),
    name="get",
)
@paginate_by_offset
class InvitesToEventList(ListAPIView):
    """
    List of my invitations to friends

    This endpoint allows the user to
    view all of his event friends.
    """

    serializer_class: Type[Serializer] = InvitesToFriendsListSerializer
    queryset: QuerySet[InviteToFriends] = InviteToFriends.get_all().filter(
        status=InviteToFriends.Status.WAITING
    )

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[InviteToFriends]:
        return self.queryset.filter(recipient=self.request.user)
