from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin,DeleteModelMixin


from .models import Notification
from .serializers import NotificationSerializer

class NotificationConsumer(ListModelMixin,DeleteModelMixin,GenericAsyncAPIConsumer):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class UserNotificationsConsumer(GenericAsyncAPIConsumer,ListModelMixin,DeleteModelMixin):
    pass