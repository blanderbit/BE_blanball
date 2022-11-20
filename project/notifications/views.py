import json
from typing import Any, Type

from config.openapi import skip_param_query
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from events.services import (
    skip_objects_from_response_by_id,
)
from notifications.constants.errors import (
    CONFIG_FILE_ERROR,
    MAINTENANCE_CAN_NOT_UPDATE_ERROR,
)
from notifications.constants.success import (
    MAINTENANCE_UPDATED_SUCCESS,
    NOTIFICATIONS_DELETED_SUCCESS,
    NOTIFICATIONS_READED_SUCCESS,
)
from notifications.models import Notification
from notifications.serializers import (
    ChangeMaintenanceSerializer,
    NotificationSerializer,
    ReadOrDeleteNotificationsSerializer,
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


@method_decorator(swagger_auto_schema(manual_parameters=[skip_param_query]), name="get")
class UserNotificationsList(ListAPIView):
    """
    This endpoint allows the user to get a
    complete list of his notifications, as
    well as sort them by newest.
    Allowed fields for sorting: 'id', '-id'
    """

    serializer_class: Type[Serializer] = NotificationSerializer
    filter_backends = [
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
    This endpoint allows the user to get the
    total number of his notifications, as well
    as the number of unread notifications.

    all_notifications_count - Number of all
        notifications
    not_read_notifications_count - Number of
        unread notifications
    """

    queryset: QuerySet[Notification] = Notification.get_all().filter()
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

    serializer_class: Type[Serializer] = ReadOrDeleteNotificationsSerializer
    queryset: QuerySet[Notification] = Notification.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            bulk_read_notifications(
                data=serializer.validated_data["ids"],
                queryset=self.queryset,
                user=request.user,
            ),
            status=HTTP_200_OK,
        )


class DeleteNotifcations(GenericAPIView):
    """
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
    then they will be read.
    """

    serializer_class: Type[Serializer] = ReadOrDeleteNotificationsSerializer
    queryset: QuerySet[Notification] = Notification.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            bulk_delete_notifications(
                data=serializer.validated_data["ids"],
                queryset=self.queryset,
                user=request.user,
            ),
            status=HTTP_200_OK,
        )


class ChangeMaintenance(GenericAPIView):
    """
    This endpoint allows you to change the
    current state of technical work in the application.
    \nIf technical work is true then the client side of the
    application will be blocked
    """

    serializer_class: Type[Serializer] = ChangeMaintenanceSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            update_maintenance(data=request.data)
            return Response(MAINTENANCE_UPDATED_SUCCESS, status=HTTP_200_OK)
        except:
            return Response(
                MAINTENANCE_CAN_NOT_UPDATE_ERROR, status=HTTP_400_BAD_REQUEST
            )


class GetMaintenance(APIView):
    """
    This endpoint allows the user to get the
    current state of the technical work
    of the application.
    If technical work is true then the
    client side of the application will be blocked
    """

    key: str = "isMaintenance"
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        try:
            with open("./config/config.json", "r") as f:
                data = f.read()
            return Response({self.key: json.loads(data)[self.key]}, status=HTTP_200_OK)
        except:
            return Response(CONFIG_FILE_ERROR, status=HTTP_400_BAD_REQUEST)


class GetCurrentVersion(GetMaintenance):
    """
    This endpoint allows any user to get
    the current version of the application.
    """

    key: str = "version"


class DeleteAllUserNotifications(APIView):
    """
    This endpoint allows the user to
    delete all his notifications at once.
    """

    queryset: QuerySet[Notification] = Notification.get_all()

    def delete(self, request: Request) -> Response:
        delete_all_user_notifications.delay(request_user_id=request.user.id)
        return Response(NOTIFICATIONS_DELETED_SUCCESS, status=HTTP_200_OK)


class ReadAllUserNotifications(APIView):
    """
    This endpoint allows the user to
    read all his notifications at once.
    """

    queryset: QuerySet[Notification] = Notification.get_all()

    def get(self, request: Request) -> Response:
        read_all_user_notifications.delay(request_user_id=request.user.id)
        return Response(NOTIFICATIONS_READED_SUCCESS, status=HTTP_200_OK)
