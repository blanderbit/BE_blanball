from .consumers import *
from .views import *

from django.urls import path


websocket_urlpatterns = [
    path('my/notifications/',UserConsumer.as_asgi())
]
