from django.urls import path
from .consumers import *
from .views import *

websocket_urlpatterns = [
    path('my/notifications/',UserConsumer.as_asgi())
]
