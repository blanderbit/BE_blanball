from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a use can get list of notifications
    path('admin/notifications/list', NotificationsList.as_view(),
        name = 'notification-list'),
    #endpoint where a use can get list of her notifications
    path('client/my/notifications/list',UserNotificationsList.as_view(),
        name = 'user-notifications-list'),
    #endpoint where a user can red her notificaions
    path('client/read/notifications',ReadNotifications.as_view(),
        name = 'user-read-notifications'),
    #endpoint where a user can  delete her her notificaions
    path('client/delete/notifications',DeleteNotifcations.as_view(),
        name = 'user-delete-notifications'),
]