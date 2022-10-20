from datetime import (date, 
    datetime,
)
from authentication.models import (
    User,
    Gender,
)
from django.db import models
from django.db.models.query import QuerySet

from django.core.validators import (
    MaxValueValidator, 
    MinValueValidator,
)
from notifications.tasks import (
    send_to_user,
)
from events.constaints import (
    INVITE_USER_NOTIFICATION, INVITE_USER_TO_EVENT_MESSAGE_TYPE,
    SEND_INVATION_ERROR, AUTHOR_CAN_NOT_INVITE_ERROR,
    SENT_INVATION_ERROR, USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR
)

from rest_framework.serializers import ValidationError
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
)

from phonenumber_field.modelfields import PhoneNumberField

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
            default=6)
    type: str = models.CharField(choices = Type.choices, max_length = 15)
    price: int = models.PositiveSmallIntegerField(null = True,blank= True, validators = [
        MinValueValidator(1)])
    price_description: str = models.CharField(max_length = 500, null = True, blank= True)
    need_form: bool = models.BooleanField()
    privacy: bool = models.BooleanField()
    duration: int = models.PositiveSmallIntegerField(choices = Duration.choices)
    forms: list = models.CharField(choices = CloseType.choices, max_length = 15)
    status: str =  models.CharField(choices = Status.choices, max_length = 10, default = 'Planned')
    current_users: User = models.ManyToManyField(User, related_name = 'current_rooms', blank = True)
    current_fans: User = models.ManyToManyField(User, related_name = 'current_views_rooms', blank = True)

    @property
    def count_current_users(self) -> int:
        return self.current_users.count()

    @property
    def count_current_fans(self) -> int:
        return self.current_fans.count()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'event'

class RequestToParticipation(models.Model):
    user: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user')
    time_created: date =  models.DateTimeField(auto_now_add = True)
    event: Event = models.ForeignKey(Event, on_delete = models.CASCADE)
    event_author: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'author')

    def __str__(self) -> str:
        return self.user.email
    
    class Meta:
        db_table = 'request_to_participation'



class InviteToEventManager(models.Manager):

    def send_invite(self, request_user: User, invite_user: User, event: Event) -> 'InviteToEvent':

        if invite_user.id == request_user.id:
            raise ValidationError(SENT_INVATION_ERROR, HTTP_403_FORBIDDEN)
        if invite_user.id == event.author.id:
            raise ValidationError(AUTHOR_CAN_NOT_INVITE_ERROR, HTTP_403_FORBIDDEN)

        if request_user.id == event.author.id or request_user.id in event.current_users.all():
            send_to_user(user = invite_user, notification_text =
                INVITE_USER_NOTIFICATION.format(user_name = invite_user.profile.name,
                inviter_name = request_user.profile.name, event_id = event.id),
                message_type = INVITE_USER_TO_EVENT_MESSAGE_TYPE, data = {
                    'event_id': event.id, 'sender_id': request_user.id})
        else:
            raise ValidationError(USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR, HTTP_403_FORBIDDEN)

        invite = self.model(recipient = invite_user, event = event, sender = request_user)
        return invite.save()



class InviteToEvent(models.Model):
    recipient: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'recipient')
    time_created: datetime = models.DateTimeField(auto_now_add = True)
    event: Event = models.ForeignKey(Event, on_delete = models.CASCADE)
    sender: User = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sender')

    objects = InviteToEventManager()

    def __repr__ (self) -> str:
        return '<InviteToEvent %s>' % self.id

    def __str__(self) -> str:
        return self.name

    def get_invite_to_event_list() -> QuerySet['InviteToEvent']:
        return InviteToEvent.objects.all().select_related('recipient', 'event', 'sender').order_by('-id')

    class Meta:
        db_table: str = 'invite_to_event'
        verbose_name: str = 'invite to event'
        verbose_name_plural: str = 'invites to event'