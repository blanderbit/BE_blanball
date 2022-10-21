from datetime import (
    date, 
    datetime,
)
import profile
from typing import Any, final
from authentication.models import (
    User,
    Gender,
)
from django.db import models
from django.core.validators import (
    MaxValueValidator, 
    MinValueValidator,
)
from django.db.models.query import QuerySet

from phonenumber_field.modelfields import PhoneNumberField

from notifications.tasks import (
    send_to_user,
)
from events.constants import (
    INVITE_USER_TO_EVENT_MESSAGE_TYPE,
    USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR, SENT_INVATION_ERROR,
    AUTHOR_CAN_NOT_INVITE_ERROR, USER_IN_BLACK_LIST_ERROR
)
from rest_framework.serializers import ValidationError
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
)

class Event(models.Model):
    '''footbal ivent model'''
    
    class Type(models.TextChoices):
        '''ivent  type choices'''
        football: str = 'Football'
        futsal: str = 'Futsal'

    class CloseType(models.TextChoices):
        shirt_front: str = 'Shirt-Front'
        t_shirt: str = 'T-Shirt'
        any: str = 'Any'

    class Status(models.TextChoices):
        planned: str = 'Planned'
        active: str = 'Active'
        finished: str = 'Finished'

    class Duration(models.IntegerChoices):
        minutes_10: int = 10
        minutes_20: int = 20
        minutes_30: int = 30
        minutes_40: int = 40
        minutes_50: int = 50
        minutes_60: int = 60
        minutes_70: int = 70
        minutes_80: int = 80
        minutes_90: int = 90
        minutes_100: int = 100
        minutes_110: int = 110
        minutes_120: int = 120
        minutes_130: int = 130
        minutes_140: int = 140
        minutes_150: int = 150
        minutes_160: int = 160
        minutes_170: int = 170
        minutes_180: int = 180

    author: User = models.ForeignKey(User, on_delete = models.CASCADE)
    name: str = models.CharField(max_length = 255)
    description: str = models.TextField()
    place: str = models.CharField(max_length = 255)
    gender: str = models.CharField(choices = Gender.choices, max_length = 10)
    date_and_time: datetime = models.DateTimeField()
    contact_number: str = PhoneNumberField(null = True, blank = True)
    need_ball: bool = models.BooleanField()
    amount_members: int = models.PositiveSmallIntegerField(validators = [
            MinValueValidator(6),
            MaxValueValidator(50)],
            default = 6)
    type: str = models.CharField(choices = Type.choices, max_length = 15)
    price: int = models.PositiveSmallIntegerField(null = True, blank= True, validators = [
        MinValueValidator(1)])
    price_description: str = models.CharField(max_length = 500, null = True, blank= True)
    need_form: bool = models.BooleanField()
    privacy: bool = models.BooleanField()
    duration: int = models.PositiveSmallIntegerField(choices = Duration.choices)
    forms: str = models.CharField(choices = CloseType.choices, max_length = 15)
    status: str =  models.CharField(choices = Status.choices, max_length = 10, default = 'Planned')
    current_users: list[User] = models.ManyToManyField(User, related_name = 'current_rooms', blank = True)
    current_fans: list[User] = models.ManyToManyField(User, related_name = 'current_views_rooms', blank = True)
    black_list: list[User] = models.ManyToManyField(User, related_name = 'black_list', blank = True)

    @property
    def count_current_users(self) -> int:
        return self.current_users.count()

    @property
    def count_current_fans(self) -> int:
        return self.current_fans.count()

    @final
    def __repr__ (self) -> str:
        return  '<Event %s>' % self.id

    @final
    def __str__(self) -> str:
        return self.name

    @final
    @staticmethod
    def get_all() -> QuerySet['Event']:
        return Event.objects.all().filter().select_related('author').prefetch_related('current_users', 'current_fans').order_by('-id')
    
    class Meta:
        db_table: str = 'event'
        verbose_name: str = 'event'
        verbose_name_plural: str = 'events'
        

class RequestToParticipation(models.Model):
    user: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user')
    time_created: datetime = models.DateTimeField(auto_now_add = True)
    event: Event = models.ForeignKey(Event, on_delete = models.CASCADE)
    event_author: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'author')

    @final
    def __repr__ (self) -> str:
        return '<RequestToParticipation %s>' % self.id

    @final
    def __str__(self) -> str:
        return self.user.email

    @final
    @staticmethod
    def get_all() -> QuerySet['RequestToParticipation']:
        return RequestToParticipation.objects.all().select_related('user', 'event_author', 'event').order_by('-id')
    
    class Meta:
        db_table: str = 'request_to_participation'
        verbose_name: str = 'request to participation'
        verbose_name_plural: str = 'requests to participation'
    

class EventTemplate(models.Model):
    author: User = models.ForeignKey(User, on_delete = models.CASCADE)
    name: str = models.CharField(max_length = 255)
    time_created: datetime = models.DateTimeField(auto_now_add = True)
    event_data: dict[str, Any] = models.JSONField()

    @property
    def count_current_users(self) -> int:
        return len(self.event_data['current_users'])

    @final
    def __repr__ (self) -> str:
        return '<EventTemplate %s>' % self.id

    @final
    def __str__(self) -> str:
        return self.name
    
    @final
    @staticmethod
    def get_all() -> QuerySet['EventTemplate']:
        return EventTemplate.objects.all().select_related('author').order_by('-id')

    class Meta:
        db_table: str = 'event_template'
        verbose_name: str = 'event template'
        verbose_name_plural: str = 'events templates'

class InviteToEventManager(models.Manager):

    def send_invite(self, request_user: User, invite_user: User, event: Event) -> 'InviteToEvent':

        if invite_user.id == request_user.id:
            raise ValidationError(SENT_INVATION_ERROR, HTTP_403_FORBIDDEN)
        if invite_user.id == event.author.id:
            raise ValidationError(AUTHOR_CAN_NOT_INVITE_ERROR, HTTP_403_FORBIDDEN)
        if invite_user in event.black_list.all():
            raise ValidationError(USER_IN_BLACK_LIST_ERROR, HTTP_403_FORBIDDEN)

        if request_user.id == event.author.id or request_user.id in event.current_users.all():
            invite = self.model(recipient = invite_user, event = event, sender = request_user)
            invite.save()
            send_to_user(user = invite_user, message_type = INVITE_USER_TO_EVENT_MESSAGE_TYPE, 
                data = {
                    'recipient': {
                        'id': invite_user.id, 
                        'name': invite_user.profile.name , 
                        'last_name': invite_user.profile.last_name,
                    },
                    'event': {
                        'id': event.id
                    },
                    'sender': {
                        'id': request_user.id,
                        'name': request_user.profile.name,
                        'last_name': request_user.profile.last_name,
                    }
                })
            return invite
        else:
            raise ValidationError(USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR, HTTP_403_FORBIDDEN)



class InviteToEvent(models.Model):
    recipient: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'recipient')
    time_created: datetime = models.DateTimeField(auto_now_add = True)
    event: Event = models.ForeignKey(Event, on_delete = models.CASCADE)
    sender: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sender')

    objects = InviteToEventManager()

    @final
    def __repr__ (self) -> str:
        return '<InviteToEvent %s>' % self.id

    @final
    def __str__(self) -> str:
        return self.recipient.profile.name

    @final
    @staticmethod
    def get_all() -> QuerySet['InviteToEvent']:
        return InviteToEvent.objects.all().select_related('recipient', 'event', 'sender').order_by('-id')

    class Meta:
        db_table: str = 'invite_to_event'
        verbose_name: str = 'invite to event'
        verbose_name_plural: str = 'invites to event'