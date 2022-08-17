from django.db import models
from authentication.models import User

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=20)
