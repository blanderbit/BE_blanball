from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a use can get list of notifications
    path('admin/notifications/list', NotificationsList.as_view(),
        name = 'notification-list'),
    #endpoint where a use can get list of her notifications
    path('client/my/notifications/list',UserNotificationsList.as_view(),
        name = 'user-notification-list'),
]
