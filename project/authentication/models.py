from .managers import *

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.serializers import ValidationError
from rest_framework import status



class Gender(models.TextChoices):
    '''gender choices'''
    man = 'Man'
    woomen = 'Woomen'


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def validate_birthday(value):
    if timezone.now().date() - value > timezone.timedelta(days=29200):
        raise ValidationError(MAX_AGE_VALUE_ERROR,status.HTTP_400_BAD_REQUEST) 
    if timezone.now().date() - value < timezone.timedelta(days=2191):
        raise ValidationError(MIN_AGE_VALUE_ERROR,status.HTTP_400_BAD_REQUEST) 

def configuration_dict():
    return {'email': True,'phone':True}

class Profile(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices =  Gender.choices,max_length=10)
    birthday = models.DateField(blank=True,null = True,validators = [validate_birthday])
    avatar = models.ImageField(null=True,blank=True,upload_to = 'media/profile')
    age = models.PositiveSmallIntegerField(null=True,blank=True)
    height = models.PositiveSmallIntegerField(null=True,blank=True)
    weight = models.PositiveSmallIntegerField(null=True,blank=True)
    position = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    about_me =  models.TextField(blank=True,null = True)
    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    '''basic user model'''
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone = PhoneNumberField(unique=True)
    is_verified = models.BooleanField(default=False)
    get_planned_events = models.CharField(max_length=10,default="1m") 
    role =  models.ForeignKey(Role,on_delete=models.CASCADE,blank=True,null = True)
    updated_at = models.DateTimeField(auto_now=True)
    raiting = models.FloatField(null = True,blank= True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null = True,related_name='user')
    configuration = models.JSONField(default = configuration_dict)


    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        access = AccessToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(access)
        }
    @property
    def group_name(self):
        return "user_%s" % self.id


class Code(models.Model):
    value = models.CharField(max_length=5,unique=True)
    life_time = models.DateTimeField(null = True,blank=True)
    type = models.CharField(max_length=20)
    user_email = models.CharField(max_length=100)
    dop_info = models.CharField(max_length=250,null = True,blank = True)

    def __str__(self):  
        return self.value


class ActiveUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.user.id

