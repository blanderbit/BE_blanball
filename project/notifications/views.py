import json
from typing import Any, Type

from api_keys.permissions import ApiKeyPermission
from config.serializers import (
    BaseBulkSerializer,
)
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from utils import skip_objects_from_response_by_id, paginate_by_offset
from notifications.constants.errors import (
    MAINTENANCE_CAN_NOT_GET_ERROR,
    MAINTENANCE_CAN_NOT_UPDATE_ERROR,
)
from notifications.constants.success import (
    MAINTENANCE_UPDATED_SUCCESS,
    NOTIFICATIONS_DELETED_SUCCESS,
    NOTIFICATIONS_READED_SUCCESS,
)
from notifications.filters import (
    NotificationsFilterSet,
)
from notifications.models import Notification
from notifications.openapi import (
    notifications_list_query_params,
)
from notifications.serializers import (
    ChangeMaintenanceSerializer,
    GetNotificationsIdsSerializer,
    NotificationSerializer,
    UserNotificationsCount,
)
from notifications.services import (
    bulk_delete_notifications,
    bulk_read_notifications,
    update_maintenance,
)
from notifications.tasks import (
    delete_all_user_notifications,
    read_all_user_notifications,
)
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView


@method_decorator(
    swagger_auto_schema(manual_parameters=notifications_list_query_params), name="get"
)
@paginate_by_offset
class UserNotificationsList(ListAPIView):
    """
    List of user notifications

    This endpoint allows the user to get a
    complete list of his notifications, as
    well as sort them by newest.
    Allowed fields for sorting: 'id', '-id'
    """

    serializer_class: Type[Serializer] = NotificationSerializer
    filterset_class = NotificationsFilterSet
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    ordering_fields: list[str] = [
        "id",
    ]
    queryset: QuerySet[Notification] = Notification.get_all()

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Notification]:
        return self.queryset.filter(user_id=self.request.user.id)


class UserNotificaitonsCount(GenericAPIView):
    """
    User notifications count

    This endpoint allows the user to get the
    total number of his notifications, as well
    as the number of unread notifications.

    all_notifications_count - Number of all
        notifications
    not_read_notifications_count - Number of
        unread notifications
    """

    queryset: QuerySet[Notification] = Notification.get_all()
    serializer_class: Type[Serializer] = UserNotificationsCount

    def get(self, request: Request) -> Response:
        data: dict[str, int] = {
            "all_notifications_count": self.queryset.filter(
                user_id=self.request.user.id
            ).count(),
            "not_read_notifications_count": self.queryset.filter(
                type=Notification.Type.UNREAD, user_id=self.request.user.id
            ).count(),
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ReadNotifications(GenericAPIView):
    """
    Read notifications

    This endpoint allows the user to
    read a certain number of notifications by ID.
    Example:
    {
        "ids": [
            1, 2, 3, 4, 5
        ]
    }
    If the user who sent the request has unread
    notifications under identifiers: 1,2,3,4,5
    then they will be read.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    queryset: QuerySet[Notification] = Notification.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            bulk_read_notifications(
                ids=serializer.validated_data["ids"],
                user=request.user,
            ),
            status=HTTP_200_OK,
        )


class DeleteNotifcations(GenericAPIView):
    """
    Delete notifications

    This endpoint allows the user to
    delete a certain number of notifications by ID.
    Example:
    {
        "ids": [
            1, 2, 3, 4, 5
        ]
    }
    If the user who sent the request has
    notifications under identifiers: 1,2,3,4,5
    then they will be delete.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    queryset: QuerySet[Notification] = Notification.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            bulk_delete_notifications(
                ids=serializer.validated_data["ids"],
                user=request.user,
            ),
            status=HTTP_200_OK,
        )


class ChangeMaintenance(GenericAPIView):
    """
    Change maintenance

    This endpoint allows you to change the
    current state of technical work in the application.
    \nIf technical work is true then the client side of the
    application will be blocked
    """

    serializer_class: Type[Serializer] = ChangeMaintenanceSerializer
    permission_classes = [
        ApiKeyPermission,
    ]

    @swagger_auto_schema(
        tags=["maintenance"],
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            update_maintenance(data=request.data)
            return Response(MAINTENANCE_UPDATED_SUCCESS, status=HTTP_200_OK)
        except FileNotFoundError:
            return Response(
                MAINTENANCE_CAN_NOT_UPDATE_ERROR, status=HTTP_400_BAD_REQUEST
            )


class GetMaintenance(APIView):
    """
    Get maintenance

    This endpoint allows the user to get the
    current state of the technical work
    of the application.
    If technical work is true then the
    client side of the application will be blocked
    """

    key: str = "isMaintenance"
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["maintenance"],
    )
    def get(self, request: Request) -> Response:
        try:
            with open("./config/config.json", "r") as f:
                data = f.read()
            return Response({self.key: json.loads(data)[self.key]}, status=HTTP_200_OK)
        except FileNotFoundError:
            return Response(MAINTENANCE_CAN_NOT_GET_ERROR, status=HTTP_400_BAD_REQUEST)


class GetCurrentVersion(GetMaintenance):
    """
    Get current version

    This endpoint allows any user to get
    the current version of the application.
    """

    key: str = "version"


class DeleteAllUserNotifications(APIView):
    """
    Delete all notifications

    This endpoint allows the user to
    delete all his notifications at once.
    """

    queryset: QuerySet[Notification] = Notification.get_all()

    def delete(self, request: Request) -> Response:
        delete_all_user_notifications.delay(request_user_id=request.user.id)
        return Response(NOTIFICATIONS_DELETED_SUCCESS, status=HTTP_200_OK)


class ReadAllUserNotifications(APIView):
    """
    Read all notifcations

    This endpoint allows the user to
    read all his notifications at once.
    """

    queryset: QuerySet[Notification] = Notification.get_all()

    def get(self, request: Request) -> Response:
        read_all_user_notifications.delay(request_user_id=request.user.id)
        return Response(NOTIFICATIONS_READED_SUCCESS, status=HTTP_200_OK)


class GetNotificationsIds(GenericAPIView):
    """
    Get user notifications ids array

    This endpoint allows the user to
    get the array of all his notifications ids
    """

    queryset: QuerySet[Notification] = Notification.get_all()
    serializer_class: Type[Serializer] = GetNotificationsIdsSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "ids": self.queryset.filter(user=request.user).values_list(
                    "id", flat=True
                )[: serializer.validated_data["count"]]
            }
        )
