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

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    small_disc = models.CharField(max_length=255)
    full_disc = models.TextField()
    place = models.CharField(max_length=255)
    gender =  models.CharField(choices=Gender.choices,max_length=10)
    date_and_time = models.DateTimeField()
    contact_number = PhoneNumberField(null=True,blank=True)
    need_ball = models.BooleanField()
    amount_members = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(6),MaxValueValidator(50)],default=6)
    type = models.CharField(choices=Type.choices,max_length=15)
    price = models.PositiveSmallIntegerField(null = True,blank= True, validators=[MinValueValidator(1)])
    price_description = models.CharField(max_length=500,null = True,blank= True)
    need_form = models.BooleanField()
    privacy = models.BooleanField()
    duration = models.PositiveSmallIntegerField(choices = Duration.choices)
    forms = models.CharField(choices=CloseType.choices,max_length=15)
    status =  models.CharField(choices=Status.choices,max_length=10,default = "Planned")
    current_users = models.ManyToManyField(User, related_name="current_rooms",blank=True)
    fans =  models.ManyToManyField(User, related_name="current_views_rooms",blank=True)

    @property
    def count_current_users(self):
        return self.current_users.count()

    @property
    def count_fans(self):
        return self.fans.count()

    def __str__(self):
        return self.name

class RequestToParticipation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    time_created =  models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    event_author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    uproved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email