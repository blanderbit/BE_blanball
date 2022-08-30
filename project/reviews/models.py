from django.db import models
from authentication.models import User
from django.core.validators import MaxValueValidator

class Review(models.Model):
    email = models.EmailField(max_length=255,db_index=True)
    text =  models.CharField(max_length=200)
    time_created = models.DateTimeField(auto_now_add=True)
    stars =  models.PositiveSmallIntegerField(MaxValueValidator(5))
    user =  models.ForeignKey(User,on_delete=models.PROTECT,related_name='reviews')

    def __str__(self):
        return self.email
        
