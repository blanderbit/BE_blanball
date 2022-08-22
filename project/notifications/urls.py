from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one notification
    path('client/notification/create',CreateNotification.as_view(),
        name = 'notification-event'),
    #endpoint where a use can get list of notifications
    path('admin/notifications/list', NotificationsList.as_view(),
        name = 'notification-list'),
    #endpoint where a use can get list of her notifications
    path('admin/my/notifications/list',UserNotificationsList.as_view(),
        name = 'user-notification-list'),
]