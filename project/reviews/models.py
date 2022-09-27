from datetime import datetime
from authentication.models import User

from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

class Review(models.Model):
    email:str = models.EmailField(max_length=255,db_index=True)
    text:str =  models.CharField(max_length=200)
    time_created:datetime = models.DateTimeField(auto_now_add=True)
    stars:int =  models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    user:User =  models.ForeignKey(User,on_delete=models.PROTECT,related_name='reviews')

    def __str__(self) -> str:
        return self.email
        
