from datetime import date, datetime

from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.validators import(
    MaxValueValidator, 
    MinValueValidator,
)
from django.contrib.auth.models import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import(
    RefreshToken,
    AccessToken,
)
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

# from storages.backends.ftp import FTPStorage


from project.constaints import MIN_AGE_VALUE_ERROR,MAX_AGE_VALUE_ERROR

class UserManager(BaseUserManager):
    '''user manager'''
    def create_user(self, email: str,phone: str, password=None,*agrs,**kwargs):
        user = self.model(phone=phone,email=self.normalize_email(email),*agrs,**kwargs)
        user.set_password(password)
        user.role = "User"
        user.save()
        return user

class Gender(models.TextChoices):
    '''gender choices'''
    man: str = 'Man'
    woomen: str = 'Woomen'


class Position(models.TextChoices):
    GK: str = 'Вратар'
    LB: str = 'Лівий захисник'
    RB: str = 'Правий захисник'
    CB: str = 'Центральний захисник'
    LWB: str = 'Лівий фланговий захисник'
    RWB: str = 'Правий фланговий захисник'
    CDM: str = 'Центральний опорний півзахисник'
    CM: str = 'Центральний півзахисник'
    CAM: str = 'Центральний атакуючий півзахисник'
    RM: str = 'Правий півзахисник'
    LM: str = 'Лівий півзахисник'
    RW: str = 'Правий фланговий атакуючий'
    LW: str = 'Лівий фланговий атакуючий'
    RF: str = 'Правий форвард' 
    CF: str = 'Центральний форвард'
    LF: str = 'Лівий форвард' 
    ST: str = 'Форвард'

class Role(models.TextChoices):
    '''role choices'''
    user: str = 'User'
    admin: str = 'Admin'

def validate_birthday(value: date) -> ValidationError:
    if timezone.now().date() - value > timezone.timedelta(days=29200):
        raise ValidationError(MAX_AGE_VALUE_ERROR,HTTP_400_BAD_REQUEST) 
    if timezone.now().date() - value < timezone.timedelta(days=2191):
        raise ValidationError(MIN_AGE_VALUE_ERROR,HTTP_400_BAD_REQUEST) 

def configuration_dict() -> dict:
    return {'email': True,'phone':True,'send_email':True}

class Profile(models.Model):
    name: str = models.CharField(max_length=255,)
    last_name: str = models.CharField(max_length=255,)
    gender: str = models.CharField(choices = Gender.choices,max_length=10)
    birthday: date = models.DateField(blank=True,null = True,validators = [validate_birthday])
    avatar: Image = models.ImageField(null=True,blank=True,upload_to='srv/sftp/')
    age: int = models.PositiveSmallIntegerField(null=True,blank=True)
    height: int = models.PositiveSmallIntegerField(null=True,blank=True,validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ])
    weight: int = models.PositiveSmallIntegerField(null=True,blank=True,validators=[
            MinValueValidator(30),
            MaxValueValidator(210),
        ])
    position: str = models.CharField(choices = Position.choices,max_length=255,null=True,blank=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    about_me: str =  models.TextField(blank=True,null = True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'user_profile'


class User(AbstractBaseUser):
    '''basic user model'''
    email: str = models.EmailField(max_length=255, unique=True, db_index=True)
    phone: str = PhoneNumberField(unique=True,)
    is_verified: bool = models.BooleanField(default=False,)
    get_planned_events: str = models.CharField(max_length=10,default="1m") 
    role: str = models.CharField(choices = Role.choices,max_length=10,blank=True,null=True)
    updated_at: str = models.DateTimeField(auto_now=True,)
    raiting: float = models.FloatField(null = True,blank= True)
    profile: Profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null = True,related_name='user')
    configuration: dict = models.JSONField(default = configuration_dict,)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self) -> dict:
        refresh: RefreshToken = RefreshToken.for_user(self)
        access: AccessToken = AccessToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(access)
        }
    @property
    def group_name(self) -> str:
        return "user_%s" % self.id

    class Meta:
        db_table = 'user'


class Code(models.Model):
    verify_code: str = models.CharField(max_length=5,unique=True)
    life_time: datetime = models.DateTimeField(null = True,blank=True)
    type: str = models.CharField(max_length=20)
    user_email: str = models.CharField(max_length=255,)
    dop_info: str = models.CharField(max_length=255,null = True,blank = True)

    def __str__(self) -> str:  
        return self.verify_code
    
    class Meta:
        db_table = 'code'


class ActiveUser(models.Model):
    user: User = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email
    
    class Meta:
        db_table = 'active_user'

