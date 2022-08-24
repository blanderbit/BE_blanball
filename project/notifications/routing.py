from django.urls import path
from .consumers import *
from djangochannelsrestframework.consumers import view_as_consumer
from .views import *

websocket_urlpatterns = [
    path('ws/<str:event_name>/',KafkaConsumer.as_asgi())
]