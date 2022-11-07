import json
from typing import Any, Type

from django.db.models.query import QuerySet
from notifications.constant.errors import (
    CONFIG_FILE_ERROR,
    MAINTENANCE_CAN_NOT_UPDATE_ERROR,
)
from notifications.constant.success import (
    MAINTENANCE_UPDATED_SUCCESS,
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
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from config.yasg import skip_param
from events.services import skip_objects_from_response_by_id


class NotificationsList(ListAPIView):
    serializer_class: Type[Serializer] = NotificationSerializer
    filter_backends = [OrderingFilter, ]
    ordering_fields: list[str] = ['id', ]
    queryset: QuerySet[Notification] = Notification.get_all()

@method_decorator(swagger_auto_schema(manual_parameters = [skip_param]), name  = 'get')
class UserNotificationsList(NotificationsList):
    
    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Notification]:
        return self.queryset.filter(user_id = self.request.user.id)

class UserNotificaitonsCount(GenericAPIView):
    queryset: QuerySet[Notification] = Notification.get_all().filter()
    serializer_class: Type[Serializer] = UserNotificationsCount

    def get(self, request: Request) -> Response:
        data: dict[str, int] = {
            'all_notifications_count': self.queryset.filter(user_id = self.request.user.id).count(),
            'not_read_notifications_count': self.queryset.filter(type = Notification.Type.UNREAD, user_id = self.request.user.id).count()
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data)


class ReadNotifications(GenericAPIView):
    serializer_class: Type[Serializer] = ReadOrDeleteNotificationsSerializer
    queryset: QuerySet[Notification] = Notification.get_all()
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)        
        return Response(bulk_read_notifications(data = serializer.validated_data['ids'],
            queryset = self.queryset), status = HTTP_200_OK)

class DeleteNotifcations(GenericAPIView):
    serializer_class: Type[Serializer] = ReadOrDeleteNotificationsSerializer
    queryset: QuerySet[Notification] = Notification.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(bulk_delete_notifications(data = serializer.validated_data['ids'],
            queryset = self.queryset, user = request.user), status = HTTP_200_OK)

class ChangeMaintenance(GenericAPIView):
    serializer_class: Type[Serializer] = ChangeMaintenanceSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            update_maintenance(data = request.data)
            return Response(MAINTENANCE_UPDATED_SUCCESS, status = HTTP_200_OK)
        except:
            return Response(MAINTENANCE_CAN_NOT_UPDATE_ERROR, status = HTTP_400_BAD_REQUEST)

class GetMaintenance(APIView):
    key: str = 'isMaintenance'
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        try:
            with open('./config/config.json', 'r') as f:
                data = f.read()
            return Response({self.key: json.loads(data)[self.key]}, status = HTTP_200_OK)
        except:
            return Response(CONFIG_FILE_ERROR, status = HTTP_400_BAD_REQUEST)

class GetCurrentVersion(GetMaintenance):
    key: str = 'version'