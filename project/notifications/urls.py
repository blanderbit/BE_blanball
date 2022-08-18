from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user can check her notifications 
    path('notifications/client/my/notifications ', UserNotificationsList.as_view(),
        name = 'user-notifications'),
]