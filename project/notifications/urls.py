from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one notification
    path('client/notification/create',CreateNotification.as_view(),
        name = 'notification-event'),
]