from notifications.consumers import UserConsumer

from django.urls import path


websocket_urlpatterns = [
    path('my/notifications/',UserConsumer.as_asgi(), 
        name = 'user-notifications')
]