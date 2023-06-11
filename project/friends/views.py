from typing import Any, Type, final

from config.openapi import (
    offset_query,
    skip_param_query,
)
from config.serializers import BaseBulkSerializer
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from friends.filters import (
    MY_FRIENDS_LIST_ORDERING_FIELDS,
    MY_FRIENDS_LIST_SEARCH_FIELDS,
    MyFriendsListFilterSet,
)
from friends.models import Friend, InviteToFriends
from friends.openapi import (
    my_friends_list_query_params,
)
from friends.serializers import (
    BulkAcceptOrDeclineInvitionsToFriendsSerializer,
    InvitesToFriendsListSerializer,
    MyFriendsListSerializer,
)
from friends.services import (
    bulk_accept_or_decline_invitions_to_friends,
    invite_users_to_friends,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from utils import (
    paginate_by_offset,
    skip_objects_from_response_by_id,
)


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
    ),
    name="get",
)
@paginate_by_offset
class InvitesToFriendsList(ListAPIView):
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


class InviteUsersToFriends(GenericAPIView):
    """
    Invite user to friends

    This endpoint allows the author of the event
    and the user who is a participant in the event
    to send invitations to participate in this event
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = invite_users_to_friends(
            users_ids=serializer.validated_data["ids"], request_user=request.user
        )
        return Response(data, status=HTTP_200_OK)


class BulkAcceptOrDeclineInvitesToFriends(GenericAPIView):
    """
    Accepting/declining invitations to friends

    This endpoint gives the user the ability to
    accept or decline invitations to friends
    """

    serializer_class: Type[Serializer] = BulkAcceptOrDeclineInvitionsToFriendsSerializer
    queryset: QuerySet[InviteToFriends] = InviteToFriends.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, int] = bulk_accept_or_decline_invitions_to_friends(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_200_OK)
