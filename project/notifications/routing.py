from django.urls import path
from .consumers import *
from djangochannelsrestframework.consumers import view_as_consumer
from .views import *

websocket_urlpatterns = [
    path('my/notifications/',UserConsumer.as_asgi())
]
