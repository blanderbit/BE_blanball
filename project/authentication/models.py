import os
import uuid

from datetime import date, datetime

from typing import Any, final

from PIL import Image

from django.db import models
from django.db.models.query import QuerySet

from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.validators import (
    MaxValueValidator, 
    MinValueValidator,
)
from django.contrib.auth.models import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import (
    RefreshToken,
    AccessToken,
)
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from authentication.constant.errors import (
    MIN_AGE_VALUE_ERROR, MAX_AGE_VALUE_ERROR
)


class UserManager(BaseUserManager):
    '''user manager'''
    @final
    def create_user(self, email: str, phone: str, password: None = None, *agrs: Any, **kwargs: Any) -> 'User':
        user = self.model(phone = phone, email = self.normalize_email(email), *agrs, **kwargs)
        user.set_password(password)
        user.role = 'User'
        user.save()
        return user

class Gender(models.TextChoices):
    '''gender choices'''
    MAN: str = 'Man'
    WOOMAN: str = 'Wooman'


class Position(models.TextChoices):
    GK: str = 'GK'
    LB: str = 'LB'
    RB: str = 'RB'
    CB: str = 'CB'
    LWB: str = 'LWB'
    RWB: str = 'RWB'
    CDM: str = 'CDM'
    CM: str = 'CM'
    CAM: str = 'CAM'
    RM: str = 'RM'
    LM: str = 'LM'
    RW: str = 'RW'
    LW: str = 'LW'
    RF: str = 'RF' 
    CF: str = 'CF'
    LF: str = 'LF' 
    ST: str = 'ST'


class Role(models.TextChoices):
    '''role choices'''
    USER: str = 'User'
    ADMIN: str = 'Admin'

def validate_birthday(value: date) -> None:
    if timezone.now().date() - value > timezone.timedelta(days = 29200):
        raise ValidationError(MAX_AGE_VALUE_ERROR, HTTP_400_BAD_REQUEST) 
    if timezone.now().date() - value < timezone.timedelta(days = 2191):
        raise ValidationError(MIN_AGE_VALUE_ERROR, HTTP_400_BAD_REQUEST) 

@final
def configuration_dict() -> dict[str, bool]:
    return {'email': True, 'phone': True, 'send_email': True}

def image_file_name(instance, filename: str) -> str:
    filename: uuid.UUID = (uuid.uuid4())

    return os.path.join('users', str(filename))

class Profile(models.Model):
    name: str = models.CharField(max_length = 255)
    last_name: str = models.CharField(max_length = 255)
    gender: str = models.CharField(choices = Gender.choices, max_length = 10)
    birthday: date = models.DateField(blank = True, null = True, validators = [validate_birthday])
    avatar: Image = models.ImageField(null = True, blank=True, upload_to = image_file_name)
    age: int = models.PositiveSmallIntegerField(null = True, blank = True)
    height: int = models.PositiveSmallIntegerField(null = True, blank = True, validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ])
    weight: int = models.PositiveSmallIntegerField(null = True, blank = True, validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ])
    position: str = models.CharField(choices = Position.choices, max_length = 255, null = True, blank = True)
    created_at: datetime = models.DateTimeField(auto_now_add = True)
    about_me: str =  models.TextField(blank = True, null = True)

    @final
    def __repr__ (self) -> str:
        return '<Profile %s>' % self.id

    @final
    def __str__(self) -> str:
        return self.name


    class Meta:
        db_table: str = 'profile'
        verbose_name: str = 'profile'
        verbose_name_plural: str = 'profiles'


class User(AbstractBaseUser):
    '''basic user model'''
    email: str = models.EmailField(max_length = 255, unique = True, db_index = True)
    phone: str = PhoneNumberField(unique = True)
    is_verified: bool = models.BooleanField(default = False)
    is_online: bool = models.BooleanField(default = False)
    get_planned_events: str = models.CharField(max_length = 10, default = '1m') 
    role: str = models.CharField(choices = Role.choices, max_length = 10, blank = True, null = True)
    updated_at: str = models.DateTimeField(auto_now = True)
    raiting: float = models.FloatField(null = True, blank= True)
    profile: Profile = models.ForeignKey(Profile, on_delete = models.CASCADE, blank = True, null = True, related_name = 'user')
    configuration: dict = models.JSONField(default = configuration_dict)

    USERNAME_FIELD: str = 'email'

    objects = UserManager()

    @final
    def __repr__ (self) -> str:
        return '<User %s>' % self.id

    @final
    def __str__(self) -> str:
        return self.email

    @final
    @staticmethod
    def get_all() -> QuerySet['User']:
        return User.objects.select_related('profile').order_by('-id')

    @final
    def tokens(self) -> dict[str, str]:
        refresh: RefreshToken = RefreshToken.for_user(self)
        access: AccessToken = AccessToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(access)
        }

    @property
    def group_name(self) -> str:
        return 'user_%s' % self.id

    class Meta:
        db_table: str = 'user'
        verbose_name: str = 'user'
        verbose_name_plural: str = 'users'


class Code(models.Model):
    verify_code: str = models.CharField(max_length = 5, unique = True)
    life_time: datetime = models.DateTimeField(null = True, blank = True)
    type: str = models.CharField(max_length = 20)
    user_email: str = models.CharField(max_length = 255)
    dop_info: str = models.CharField(max_length = 255, null = True, blank = True)

    @final
    def __repr__ (self) -> str:
        return '<Code %s>' % self.id

    @final
    def __str__(self) -> str:  
        return self.verify_code
    
    class Meta:
        db_table: str = 'code'
        verbose_name: str = 'code'
        verbose_name_plural: str = 'codes'