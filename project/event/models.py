from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import User

class Event(models.Model):
    '''footbal ivent model'''
    class Gender(models.TextChoices):
        '''ivent gender choices'''
        man = 'Man'
        woomen = 'Woomen'
        
    class Type(models.TextChoices):
        '''ivent  type choices'''
        football = 'Football'
        futsal = 'Futsal'

    author = models.ForeignKey(User,on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    small_disc = models.CharField(max_length=500)
    place = models.CharField(max_length=100)
    gender =  models.CharField(choices=Gender.choices,max_length=100)
    date_and_time = models.DateTimeField()
    contact_number = PhoneNumberField()
    need_ball = models.BooleanField()
    amount_members = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(1),MaxValueValidator(50)])
    type = models.CharField(choices=Type.choices,max_length=100)
    price = models.PositiveSmallIntegerField()
    price_description = models.CharField(max_length=500)
    need_form = models.BooleanField()
    team1_form_color = models.CharField(max_length=50,null = True,blank= True)
    team2_form_color = models.CharField(max_length=50,null = True,blank= True)

    def __str__(self):
        return self.name
