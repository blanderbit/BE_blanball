from django.db import models
from authentication.models import User



class Notification(models.Model):

    class Status(models.TextChoices):
        '''gender choices'''
        sent = 'Sent'
        read = 'Read'

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(choices =  Status.choices,max_length=10,default="Sent")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text