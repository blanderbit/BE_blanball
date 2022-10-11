import json
from typing import Any

from notifications.serializers import (
    NotificationSerializer,
    ReadOrDeleteNotificationsSerializer,
    ChangeMaintenanceSerializer,
)
from notifications.models import Notification
from project.pagination import CustomPagination

from django.db.models.query import QuerySet

from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
)

from notifications.services import (
    bulk_delete_notifications,
    update_maintenance,
    bulk_read_notifications,
)

from notifications.constaints import (MAINTENANCE_UPDATED_SUCCESS, MAINTENANCE_CAN_NOT_UPDATE_ERROR, CONFIG_FILE_ERROR)

class NotificationsList(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    filter_backends = (OrderingFilter, )
    ordering_fields = ('id', )
    queryset = Notification.objects.all().select_related('user').order_by('-id')

class UserNotificationsList(NotificationsList):
       
    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(user_id = self.request.user.id)

class ReadNotifications(GenericAPIView):
    serializer_class = ReadOrDeleteNotificationsSerializer
    queryset = Notification.objects.all()
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)        
        return Response(bulk_read_notifications(data = serializer.validated_data['notifications'],
            queryset = self.queryset), status = HTTP_200_OK)

class DeleteNotifcations(GenericAPIView):
    serializer_class = ReadOrDeleteNotificationsSerializer
    queryset = Notification.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(bulk_delete_notifications(data = serializer.validated_data['notifications'],
            queryset = self.queryset, user = request.user), status = HTTP_200_OK)

class ChangeMaintenance(GenericAPIView):
    serializer_class = ChangeMaintenanceSerializer

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

    def get(self, request: Request) -> Response:
        try:
            with open('./project/config.json', 'r') as f:
                data = f.read()
            return Response({self.key: json.loads(data)[self.key]}, status = HTTP_200_OK)
        except:
            return Response(CONFIG_FILE_ERROR, status = HTTP_400_BAD_REQUEST)

class GetCurrentVersion(GetMaintenance):
    key: str = 'version'