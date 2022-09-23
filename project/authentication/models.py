from datetime import date, datetime
from .managers import *

from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.serializers import ValidationError
from rest_framework import status



class Gender(models.TextChoices):
    '''gender choices'''
    man = 'Man'
    woomen = 'Woomen'


class Position(models.TextChoices):
    GK = 'Вратар'
    LB = 'Лівий захисник'
    RB = 'Правий захисник'
    CB = 'Центральний захисник'
    LWB = 'Лівий фланговий захисник'
    RWB = 'Правий фланговий захисник'
    CDM = 'Центральний опорний півзахисник'
    CM = 'Центральний півзахисник'
    CAM = 'Центральний атакуючий півзахисник'
    RM = 'Правий півзахисник'
    LM = 'Лівий півзахисник'
    RW = 'Правий фланговий атакуючий'
    LW = 'Лівий фланговий атакуючий'
    RF = 'Правий форвард' 
    CF = 'Центральний форвард'
    LF = 'Лівий форвард' 
    ST = 'Форвард'

class Role(models.TextChoices):
    '''role choices'''
    user = 'User'
    admin = 'Admin'

def validate_birthday(value:date) -> ValidationError:
    if timezone.now().date() - value > timezone.timedelta(days=29200):
        raise ValidationError(MAX_AGE_VALUE_ERROR,status.HTTP_400_BAD_REQUEST) 
    if timezone.now().date() - value < timezone.timedelta(days=2191):
        raise ValidationError(MIN_AGE_VALUE_ERROR,status.HTTP_400_BAD_REQUEST) 

def configuration_dict() -> dict:
    return {'email': True,'phone':True,'send_email':True}

class Profile(models.Model):
    name:str = models.CharField(max_length=255)
    last_name:str = models.CharField(max_length=255)
    gender:str = models.CharField(choices = Gender.choices,max_length=10)
    birthday:date = models.DateField(blank=True,null = True,validators = [validate_birthday])
    avatar:Image = models.ImageField(null=True,blank=True,upload_to = 'media/profile')
    age:int = models.PositiveSmallIntegerField(null=True,blank=True)
    height:int = models.PositiveSmallIntegerField(null=True,blank=True,validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ])
    weight:int = models.PositiveSmallIntegerField(null=True,blank=True,validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ])
    position:str = models.CharField(choices = Position.choices,max_length=255,null=True,blank=True)
    created_at:datetime = models.DateTimeField(auto_now_add=True)
    about_me:str =  models.TextField(blank=True,null = True)
    
    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser):
    '''basic user model'''
    email:str = models.EmailField(max_length=255, unique=True, db_index=True)
    phone:str = PhoneNumberField(unique=True)
    is_verified:bool = models.BooleanField(default=False)
    get_planned_events:str = models.CharField(max_length=10,default="1m") 
    role:str = models.CharField(choices = Role.choices,max_length=10,blank=True,null=True)
    updated_at:str = models.DateTimeField(auto_now=True)
    raiting:float = models.FloatField(null = True,blank= True)
    profile:Profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null = True,related_name='user')
    configuration:dict = models.JSONField(default = configuration_dict)


    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self) -> dict:
        refresh:RefreshToken = RefreshToken.for_user(self)
        access:AccessToken = AccessToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(access)
        }
    @property
    def group_name(self) -> str:
        return "user_%s" % self.id


class Code(models.Model):
    verify_code:str = models.CharField(max_length=5,unique=True)
    life_time:datetime = models.DateTimeField(null = True,blank=True)
    type:str = models.CharField(max_length=20)
    user_email:str = models.CharField(max_length=100)
    dop_info:str = models.CharField(max_length=250,null = True,blank = True)

    def __str__(self) -> str:  
        return self.verify_code


class ActiveUser(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email

