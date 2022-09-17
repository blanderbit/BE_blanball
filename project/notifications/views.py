import json
from webbrowser import GenericBrowser

from .tasks import send_to_user

from .serializers import *
from .models import *
from project.constaints import *
from project.services import CustomPagination

from rest_framework import generics,status,filters
from rest_framework.response import Response


class NotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id',)
    queryset = Notification.objects.all().order_by('-id')


class UserNotificationsList(NotificationsList):     
    def get_queryset(self):
        return self.queryset.filter(user_id = self.request.user.id)

class ReadNotifications(generics.GenericAPIView):
    serializer_class = ReadOrDeleteNotificationsSerializer
    queryset = Notification.objects.all()
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        read = [] 
        not_read = []
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
        return Response({"read success": read, "read error": not_read},status=status.HTTP_200_OK)
            

class DeleteNotifcations(generics.GenericAPIView):
    serializer_class = ReadOrDeleteNotificationsSerializer
    queryset = Notification.objects.all()

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deleted = [] 
        not_deleted = []
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
        return Response({"delete success": deleted, "delete error":  not_deleted},status=status.HTTP_200_OK)



class ChangeMaintenance(generics.GenericAPIView):
    serializer_class = ChangeMaintenanceSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        try:
            with open('./project/project/config.json', 'w') as f:
                json.dump(data,f)
                for user in User.objects.all():
                    if data["isMaintenance"] == True:
                        notification_text=MAINTENANCE_TRUE_NOTIFICATION_TEXT.format(username=user.profile.name,last_name=user.profile.last_name)
                    else:
                        notification_text=MAINTENANCE_FALSE_NOTIFICATION_TEXT.format(username=user.profile.name,last_name=user.profile.last_name)
                    send_to_user(user = user,notification_text=notification_text,message_type=CHANGE_MAINTENANCE_MESSAGE_TYPE)
            return Response(MAINTENANCE_UPDATED_SUCCESS,status=status.HTTP_200_OK)
        except:
            return Response(MAINTENANCE_CAN_NOT_UPDATE_ERROR,status=status.HTTP_400_BAD_REQUEST)


class GetMaintenance(generics.GenericAPIView):
    serializer_class = ChangeMaintenanceSerializer

    def get(self,request):
        try:
            with open('./project/project/config.json', 'r') as f:
                data = f.read()
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response()