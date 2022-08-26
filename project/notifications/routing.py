from django.urls import path
from .consumers import *
from djangochannelsrestframework.consumers import view_as_consumer
from .views import *

websocket_urlpatterns = [
    path('ws/<str:room_name>/',KafkaConsumer.as_asgi()),
    path('ws/e/<str:user_group_name>/',UserConsumer.as_asgi())
]
