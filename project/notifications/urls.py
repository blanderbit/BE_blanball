from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from notifications.views import (
    ChangeMaintenance,
    DeleteAllUserNotifications,
    DeleteNotifcations,
    GetCurrentVersion,
    GetMaintenance,
    NotificationsList,
    ReadAllUserNotifications,
    ReadNotifications,
    UserNotificaitonsCount,
    UserNotificationsList,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path(
        "admin/notifications/list",
        NotificationsList.as_view(),
        name="notifications-list",
    ),
    path(
        "client/my/notifications/list",
        UserNotificationsList.as_view(),
        name="user-notifications-list",
    ),
    path(
        "client/my/not-read/notifications/count",
        UserNotificaitonsCount.as_view(),
        name="user-not-read-notifications-count",
    ),
    path(
        "client/read/all/notifications",
        ReadAllUserNotifications.as_view(),
        name="read-all-notifications",
    ),
    path(
        "client/read/notifications",
        ReadNotifications.as_view(),
        name="bulk-read-notifications",
    ),
    path(
        "client/delete/notifications",
        DeleteNotifcations.as_view(),
        name="bulk-delete-notifications",
    ),
    path(
        "client/delete/all/notifications",
        DeleteAllUserNotifications.as_view(),
        name="delete-all-notifications",
    ),
    path(
        "admin/change/maintenance",
        ChangeMaintenance.as_view(),
        name="change-maintenance",
    ),
    path("admin/get/maintenance", GetMaintenance.as_view(), name="get-maintenance"),
    path(
        "admin/get/current/version",
        GetCurrentVersion.as_view(),
        name="get-current-version",
    ),
]
