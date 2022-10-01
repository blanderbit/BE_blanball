from datetime import datetime
from authentication.models import User

from django.db import models


class Notification(models.Model):

    class Type(models.TextChoices):
        '''gender choices'''
        unread: str = 'Unread'
        read: str = 'Read'

    user: User = models.ForeignKey(User,on_delete=models.CASCADE)
    notification_text: str = models.CharField(max_length=100)
    type: str = models.CharField(choices = Type.choices,max_length=6,default='Unread')
    time_created: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.notification_text

    class Meta:
        db_table = 'notification'
