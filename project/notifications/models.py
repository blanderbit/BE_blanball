from wsgiref.simple_server import demo_app
from django.db import models
from authentication.models import User


class Type(models.TextChoices):
    '''gender choices'''
    unread = 'Unread'
    read = 'Read'

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    notification_text = models.CharField(max_length=100)
    type = models.CharField(choices = Type.choices,max_length=6,default='Unread')
    date_time = models.DateTimeField(auto_now_add=True)

        
