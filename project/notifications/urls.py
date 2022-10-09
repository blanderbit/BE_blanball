from notifications.views import (
    NotificationsList,
    UserNotificationsList,
    ReadNotifications,
    DeleteNotifcations,
    ChangeMaintenance,
    GetMaintenance,
    GetCurrentVersion,
)   

from django.urls import path

urlpatterns = [
    # endpoint where user can get list of notifications
    path('admin/notifications/list', NotificationsList.as_view(),
        name='notifications-list'),
    # endpoint where a use can get list of her notifications
    path('client/my/notifications/list', UserNotificationsList.as_view(), 
        name='user-notifications-list'),
    # endpoint where user can bulk read her notificaions
    path('client/read/notifications', ReadNotifications.as_view(), 
        name='bulk-read-notifications'),
    # endpoint where user can bulk  delete her her notificaions
    path('client/delete/notifications', DeleteNotifcations.as_view(), 
        name='bulk-delete-notifications'),
    # endpoint where admin can change maintenance
    path('admin/change/maintenance', ChangeMaintenance.as_view(), 
        name='change-maintenance'),
    # endpoint where admin can get maintenance
    path('admin/get/maintenance', GetMaintenance.as_view(), 
        name='get-maintenance'),
    # endpoint where admin can get maintenance
    path('admin/get/current/version', GetCurrentVersion.as_view(), 
        name='get-current-version'),
]