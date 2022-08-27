from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .managers import *
from django.core.validators import MaxValueValidator, MinValueValidator

class Gender(models.TextChoices):
    '''gender choices'''
    man = 'Man'
    woomen = 'Woomen'


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices =  Gender.choices,max_length=10)
    birthday = models.DateField(blank=True,null = True)
    avatar = models.ImageField(null=True,blank=True)
    age = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(6),
            MaxValueValidator(80)
        ])
    height = models.PositiveSmallIntegerField(null=True,blank=True)
    weight = models.PositiveSmallIntegerField(null=True,blank=True)
    position = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    about_me =  models.TextField(blank=True,null = True)

    def __str__(self):
        return self.name


class ActiveUser(models.Model):
    user_id = models.IntegerField()

class User(AbstractBaseUser):
    '''basic user model'''
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone = PhoneNumberField(unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    role =  models.ForeignKey(Role,on_delete=models.CASCADE,blank=True,null = True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null = True)

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