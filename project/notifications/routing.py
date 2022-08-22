from django.urls import re_path
from .consumers import *
from djangochannelsrestframework.consumers import view_as_consumer
from .views import *

websocket_urlpatterns = []