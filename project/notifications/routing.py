from typing import Union

from notifications.consumers import UserConsumer

from django.urls import path
from django.urls.resolvers import (
   URLResolver, 
   URLPattern,
)

websocket_urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path('my/notifications/', UserConsumer.as_asgi(), 
        name = 'user-notifications')
]