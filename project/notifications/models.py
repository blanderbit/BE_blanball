from wsgiref.simple_server import demo_app
from django.db import models
from authentication.models import User


class Notification(models.Model):
    class Type(models.TextChoices):
        '''gender choices'''
        unread = 'Unread'
        read = 'Read'

    user = models.ForeignKey(User,on_delete=models.PROTECT)
    notification_text = models.CharField(max_length=100)
    type = models.CharField(choices = Type.choices,max_length=6,default='Unread')
    time_created = models.DateTimeField(auto_now_add=True)

        
