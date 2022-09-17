from datetime import date, datetime
from authentication.models import User,Gender

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

class Event(models.Model):
    '''footbal ivent model'''
        
    class Type(models.TextChoices):
        '''ivent  type choices'''
        football = 'Football'
        futsal = 'Futsal'

    class CloseType(models.TextChoices):
        shirt_front = 'Shirt-Front'
        t_shirt = 'T-Shirt'

    class Status(models.TextChoices):
        planned = 'Planned'
        active = 'Active'
        finished = 'Finished'

    class Duration(models.IntegerChoices):
        minutes_10 = 10
        minutes_20 = 20
        minutes_30 = 30
        minutes_40 = 40
        minutes_50 = 50
        minutes_60 = 60
        minutes_70 = 70
        minutes_80 = 80
        minutes_90 = 90
        minutes_100 = 100
        minutes_110 = 110
        minutes_120 = 120
        minutes_130 = 130
        minutes_140 = 140
        minutes_150 = 150
        minutes_160 = 160
        minutes_170 = 170
        minutes_180 = 180

    author:int = models.ForeignKey(User,on_delete=models.CASCADE)
    name:str = models.CharField(max_length=255)
    small_disc:str = models.CharField(max_length=255)
    full_disc:str = models.TextField()
    place:str = models.CharField(max_length=255)
    gender:str =  models.CharField(choices=Gender.choices,max_length=10)
    date_and_time:datetime = models.DateTimeField()
    contact_number:str = PhoneNumberField(null=True,blank=True)
    need_ball:bool = models.BooleanField()
    amount_members:int = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(6),MaxValueValidator(50)],default=6)
    type:str = models.CharField(choices=Type.choices,max_length=15)
    price:int = models.PositiveSmallIntegerField(null = True,blank= True, validators=[MinValueValidator(1)])
    price_description:str = models.CharField(max_length=500,null = True,blank= True)
    need_form:bool = models.BooleanField()
    privacy:bool = models.BooleanField()
    duration:int = models.PositiveSmallIntegerField(choices = Duration.choices)
    forms:list = models.CharField(choices=CloseType.choices,max_length=15)
    status:str =  models.CharField(choices=Status.choices,max_length=10,default = "Planned")
    current_users:list = models.ManyToManyField(User, related_name="current_rooms",blank=True)
    fans:list = models.ManyToManyField(User, related_name="current_views_rooms",blank=True)

    @property
    def count_current_users(self) -> int:
        return self.current_users.count()

    @property
    def count_fans(self) -> int:
        return self.fans.count()

    def __str__(self) -> str:
        return self.name

class RequestToParticipation(models.Model):
    user:int = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    time_created:date =  models.DateTimeField(auto_now_add=True)
    event:int = models.ForeignKey(Event,on_delete=models.CASCADE)
    event_author:int = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    uproved:bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.email