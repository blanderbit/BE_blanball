from .views import *

from django.urls import path


urlpatterns = [
    #endpoint where a use can get list of notifications
    path('admin/notifications/list', NotificationsList.as_view()),
    #endpoint where a use can get list of her notifications
    path('client/my/notifications/list',UserNotificationsList.as_view()),
    #endpoint where a user can red her notificaions
    path('client/read/notifications',ReadNotifications.as_view()),
    #endpoint where a user can  delete her her notificaions
    path('client/delete/notifications',DeleteNotifcations.as_view()),
]