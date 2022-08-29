from .serializers import *
from .models import *
from rest_framework import generics,permissions,response,status
from project.services import CustomPagination

class NotificationsList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()


class UserNotificationsList(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Notification.objects.all()
     
    def get_queryset(self):
        return self.queryset.filter(user_id = self.request.user.id).order_by('-date_time')

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        for notification in page:
            notification.type = 'Read'
            notification.save()

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

