import re
from secrets import choice
from selectors import EVENT_READ
from typing import Any, Union
from collections import OrderedDict
import pandas

from django.utils import timezone
from django.db.models.query import QuerySet

from rest_framework.serializers import ValidationError,Serializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from authentication.models import User
from events.models import (
    Event,
    RequestToParticipation,
)
from events.constaints import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR, EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, 
    ALREADY_SENT_REQUEST_TO_PARTICIPATE, NEW_USER_ON_THE_EVENT_NOTIFICATION, NEW_USER_ON_THE_EVENT_MESSAGE_TYPE,
    RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION, RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE,
    INVITE_USER_TO_EVENT_MESSAGE_TYPE, INVITE_USER_NOTIFICATION, SENT_INVATION_ERROR,
    GET_PLANNED_EVENTS_ERROR, AUTHOR_CAN_NOT_INVITE_ERROR, 
)
from notifications.tasks import send_to_user

from authentication.constaints import (
    NO_SUCH_USER_ERROR,
)

def event_create(data: Union[dict[str, Any], OrderedDict[str, Any]], request_user: User) -> dict[str, Any]:
    data: dict[str, Any] = dict(data)
    for user in data['current_users']:
        if user.email == request_user.email:
            raise ValidationError(SENT_INVATION_ERROR, HTTP_400_BAD_REQUEST)
        send_to_user(user = user, notification_text = INVITE_USER_NOTIFICATION.format(
        user_name = request_user.profile.name, event_name = data['name']),
        message_type = INVITE_USER_TO_EVENT_MESSAGE_TYPE)
    data.pop('current_users')
    try:
        contact_number: str = data['contact_number']
    except:
        contact_number: str = str(User.objects.get(id = request_user.id).phone)
    data['contact_number'] = contact_number
    data['date_and_time'] = str(pandas.to_datetime(data['date_and_time'].isoformat()).round('1min').to_pydatetime())
    Event.objects.create(**data, author = request_user)
    return data

def validate_event_template(data: dict[str, Any], request_user: User) -> None:
    if data['event_data']['duration'] not in [i[0] for i in Event.Duration.choices]:
        raise ValidationError()
    if data['event_data']['forms'] not in [i[0] for i in Event.CloseType.choices]:
        raise ValidationError()

    for user in data['event_data']['current_users']:
        try:
            user: User = User.objects.get(id = user)
            if request_user.id == user.id:
                raise ValidationError(AUTHOR_CAN_NOT_INVITE_ERROR, HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            raise ValidationError(NO_SUCH_USER_ERROR, HTTP_404_NOT_FOUND)

def send_notification_to_subscribe_event_user(event: Event, notification_text: str, message_type: str) -> None:
    for user in event.current_users.all():
        send_to_user(user = user, notification_text = f'{user.profile.name},{notification_text}', 
            message_type = message_type)
    for fan in event.current_fans.all():
        send_to_user(user = fan, notification_text = f'{user.profile.name},{notification_text}', 
            message_type = message_type)

def validate_user_before_join_to_event(user: User, event: Event) -> None:
    if user.current_rooms.filter(id = event.id).exists():
        raise ValidationError(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, HTTP_400_BAD_REQUEST)
    if user.current_views_rooms.filter(id = event.id).exists():
        raise ValidationError(ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR, HTTP_400_BAD_REQUEST)
    if event.author.id == user.id:
        raise ValidationError(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, HTTP_400_BAD_REQUEST)
    if RequestToParticipation.objects.filter(user = user,event = event.id, event_author = event.author):
        raise ValidationError(ALREADY_SENT_REQUEST_TO_PARTICIPATE, HTTP_400_BAD_REQUEST)

def send_notification_to_event_author(event: Event) -> None:
    if event.amount_members > event.count_current_users:
        user_type: str = 'new'
    elif event.amount_members == event.count_current_users:
        user_type: str = 'last'
    send_to_user(user = User.objects.get(id = event.author.id), notification_text=
        NEW_USER_ON_THE_EVENT_NOTIFICATION.format(author_name = event.author.profile.name, 
        user_type = user_type,event_id = event.id),
        message_type = NEW_USER_ON_THE_EVENT_MESSAGE_TYPE)


def validate_get_user_planned_events(pk: int, request_user: User ) -> None:
    user = User.objects.get(id = pk)
    if user.configuration['show_my_planned_events'] == False and request_user.id != user.id:
        raise ValidationError(GET_PLANNED_EVENTS_ERROR, HTTP_400_BAD_REQUEST)  


def filter_event_by_user_planned_events_time(pk: int, queryset: QuerySet) -> QuerySet:
    user: User =  User.objects.get(id = pk)
    num: str = re.findall(r'\d{1,10}', user.get_planned_events)[0]
    string = re.findall(r'\D', user.get_planned_events)[0]
    if string == 'd':
        num = int(num[0])
    elif string == 'm':  
        num = int(num[0]) * 30 + int(num[0]) // 2
    elif string == 'y':
        num = int(num[0]) * 365
    finish_date = timezone.now() + timezone.timedelta(days = int(num))
    return queryset.filter(author_id = user.id, date_and_time__range = [timezone.now(), finish_date])


def bulk_delete_events(data: dict[str, Any], queryset: QuerySet, user: User) -> dict[str, list[int]]:
    deleted: list[int] = [] 
    for event_id in data['events']:
        try:
            event: Event = queryset.get(id = event_id)
            if event.author == user:
                event.delete()
                deleted.append(event_id)
        except Event.DoesNotExist:
            pass
    return {'delete success': deleted}

def bulk_accpet_or_decline(data, user: User) -> dict[str, list[int]]:
    success: list[int] = []
    for request_id in data['requests']:
        try:
            request_to_p = RequestToParticipation.objects.get(id = request_id)
            if request_to_p.event_author.id == user.id:
                if data['type'] == True:
                    response_type: str = 'accepted'
                    request_to_p.user.current_rooms.add(request_to_p.event)
                else:
                    response_type: str = 'rejected'
                success.append(request_id)
                send_to_user(user = request_to_p.user, notification_text = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION.format(
                user_name = request_to_p.user.profile.name, event_id = request_to_p.event.id, response_type = response_type),
                message_type = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                request_to_p.delete()

        except RequestToParticipation.DoesNotExist:
            pass
    return {'success': success}
