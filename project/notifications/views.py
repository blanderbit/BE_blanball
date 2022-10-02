import json

from notifications.tasks import send_to_user
from notifications.serializers import (
    NotificationSerializer,
    ReadOrDeleteNotificationsSerializer,
    ChangeMaintenanceSerializer,
)
from notifications.models import Notification
from project.constaints import *
from project.services import CustomPagination

from django.db.models.query import QuerySet

from rest_framework import generics,filters
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
from authentication.models import User


class NotificationsList(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id',)
    queryset = Notification.objects.all().select_related('user').order_by('-id')


class UserNotificationsList(NotificationsList):     
    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(user_id = self.request.user.id)

class ReadNotifications(GenericAPIView):
    serializer_class = ReadOrDeleteNotificationsSerializer
    queryset = Notification.objects.all()
    
    def post(self,request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        read:list = [] 
        not_read:list = []
        for notification in serializer.validated_data['notifications']:
            notify = self.queryset.filter(id = notification)
            if notify:
                notify = self.queryset.get(id = notification)
                if notify.type != 'Read':
                    notify.type = 'Read'
                    notify.save()
                    read.append(notification)
                else:
                    not_read.append(notification) 
            else:
                not_read.append(notification)        
        return Response({"read success": read, "read error": not_read},status=HTTP_200_OK)
            

class DeleteNotifcations(GenericAPIView):
    serializer_class = ReadOrDeleteNotificationsSerializer
    queryset = Notification.objects.all()

    def post(self,request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deleted:list = [] 
        not_deleted:list = []
        for notification in serializer.validated_data['notifications']:
            notify =  self.queryset.filter(id = notification)
            if notify:
                notify = self.queryset.get(id = notification)
                if notify.user == request.user:
                    notify.delete()
                    deleted.append(notification)
                else:
                    not_deleted.append(notification)
            else:
                not_deleted.append(notification)
        return Response({"delete success": deleted, "delete error":  not_deleted},status=HTTP_200_OK)


def update_maintenance(data: dict[str,str]):
    with open('./project/project/config.json', 'w') as f:
        json.dump(data,f)
        for user in User.objects.all():
            if data["isMaintenance"] == True:
                notification_text=MAINTENANCE_TRUE_NOTIFICATION_TEXT.format(username=user.profile.name,last_name=user.profile.last_name)
            else:
                notification_text=MAINTENANCE_FALSE_NOTIFICATION_TEXT.format(username=user.profile.name,last_name=user.profile.last_name)
            send_to_user(user = user,notification_text=notification_text,message_type=CHANGE_MAINTENANCE_MESSAGE_TYPE)

class ChangeMaintenance(GenericAPIView):
    serializer_class = ChangeMaintenanceSerializer

    def post(self,request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            update_maintenance(data=request.data)
            return Response(MAINTENANCE_UPDATED_SUCCESS,status=HTTP_200_OK)
        except:
            return Response(MAINTENANCE_CAN_NOT_UPDATE_ERROR,status=HTTP_400_BAD_REQUEST)


class GetMaintenance(APIView):
    key: str = 'isMaintenance'

    def get(self,request: Request) -> Response:
        try:
            with open('./project/project/config.json', 'r') as f:
                data = f.read()
            return Response({self.key:json.loads(data)[self.key]},status=HTTP_200_OK)
        except:
            return Response(CONFIG_FILE_ERROR,status=HTTP_400_BAD_REQUEST)

class GetCurrentVersion(GetMaintenance):
    key: str = 'version'