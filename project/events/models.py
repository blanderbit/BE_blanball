from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import User,Gender

class Event(models.Model):
    '''footbal ivent model'''
        
    class Type(models.TextChoices):
        '''ivent  type choices'''
        football = 'Football'
        futsal = 'Futsal'

    author = models.ForeignKey(User,on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    small_disc = models.CharField(max_length=200)
    full_disc = models.TextField()
    place = models.CharField(max_length=500)
    gender =  models.CharField(choices=Gender.choices,max_length=10)
    date_and_time = models.DateTimeField()
    contact_number = PhoneNumberField()
    need_ball = models.BooleanField()
    amount_members = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(6),MaxValueValidator(50)],default=6)
    type = models.CharField(choices=Type.choices,max_length=100)
    price = models.PositiveSmallIntegerField(null = True,blank= True)
    price_description = models.CharField(max_length=500,null = True,blank= True)
    need_form = models.BooleanField()
    forms = models.CharField(max_length=500)
    current_users = models.ManyToManyField(User, related_name="current_rooms",null = True, blank=True)

    def __str__(self):
        return self.name
