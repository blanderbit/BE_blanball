from django.db import models
from authentication.models import User


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    text = models.CharField(max_length=100)

    
