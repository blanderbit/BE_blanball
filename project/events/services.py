from datetime import datetime
import json
import re
from typing import Any, Optional, Union, Generator, TypeVar, Callable
from collections import OrderedDict
import pandas

from django.utils import timezone
from django.db.models.query import QuerySet

from rest_framework.serializers import ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)
from django.db import transaction

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.request import Request

from authentication.models import User
from events.models import (
    Event,
    RequestToParticipation,
    InviteToEvent,
)
from events.constaints import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR, EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, 
    ALREADY_SENT_REQUEST_TO_PARTICIPATE, EVENT_NOT_FOUND_ERROR, NEW_USER_ON_THE_EVENT_NOTIFICATION, NEW_USER_ON_THE_EVENT_MESSAGE_TYPE,
    RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION, RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE,
    INVITE_USER_TO_EVENT_MESSAGE_TYPE, INVITE_USER_NOTIFICATION, SENT_INVATION_ERROR,
    GET_PLANNED_EVENTS_ERROR, AUTHOR_CAN_NOT_INVITE_ERROR, RESPONSE_TO_THE_INVITE_TO_EVENT, 
    RESPONSE_TO_THE_INVITE_TO_EVENT_MESSAGE_TYPE,
)
from notifications.tasks import send_to_user

bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])


def bulk_delete_events(*, data: dict[str, Any], queryset: QuerySet[Event], user: User) -> bulk:
    for event_id in data:
        try:
            event: Union[Event, EventTemplate] = queryset.get(id = event_id)
            if event.author == user:
                event.delete()
                yield {'success': event_id}
        except Event.DoesNotExist:
            pass

def bulk_accept_or_decline_invites_to_events(*, data: dict[str, Union[list[int], bool]], request_user: User) -> bulk: 
    for invite_id in data['ids']:
        try:
            invite: InviteToEvent  = InviteToEvent.objects.get(id = invite_id)
            if invite.recipient.id == request_user.id:
                if invite.event.current_users.count() < invite.event.amount_members:
                    if data['type'] == True:
                        response_type: str = 'accepted'
                        if invite.event.privacy == False:
                            invite.recipient.current_rooms.add(invite.event)
                        else:
                            RequestToParticipation.objects.create(user = invite.recipient, 
                                event_id = invite.event.id, event_author = invite.event.author)
                    else:
                        response_type: str = 'declined'
                    yield {'success': invite_id}
                    send_to_user(user = invite.sender, notification_text = RESPONSE_TO_THE_INVITE_TO_EVENT.format(
                    user_name = invite.sender.profile.name, recipient_name = invite.recipient.profile.name, 
                    recipient_last_name = invite.recipient.profile.last_name, 
                    event_id = invite.event.id, response_type = response_type),
                    message_type = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                    invite.delete()

        except InviteToEvent.DoesNotExist:
            pass

def bulk_accpet_or_decline_requests_to_participation(*, data: dict[str, Union[list[int], bool]], user: User) -> bulk: 
    for request_id in data['ids']:
        try:
            request_to_p = RequestToParticipation.objects.get(id = request_id)
            if request_to_p.event_author.id == user.id:
                if data['type'] == True:
                    response_type: str = 'accepted'
                    if request_to_p.event.current_users.count() < request_to_p.event.amount_members:
                        request_to_p.user.current_rooms.add(request_to_p.event)
                else:
                    response_type: str = 'declined'
                yield {'success': request_id}
                send_to_user(user = request_to_p.user, notification_text = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION.format(
                user_name = request_to_p.user.profile.name, event_id = request_to_p.event.id, response_type = response_type),
                message_type = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                request_to_p.delete()

        except RequestToParticipation.DoesNotExist:
            pass


def event_create(*, data: Union[dict[str, Any], OrderedDict[str, Any]], request_user: User) -> dict[str, Any]:
    data = dict(data)
    users: list[int] = data['current_users']
    data.pop('current_users')
    try:
        contact_number: str = data['contact_number']
    except KeyError:
        contact_number: str = str(User.objects.get(id = request_user.id).phone)
    data['contact_number'] = contact_number
    data['date_and_time'] = pandas.to_datetime(data['date_and_time'].isoformat()).round('1min').to_pydatetime()
    with transaction.atomic():
        event: Event = Event.objects.create(**data, author = request_user)
        for user in users:
            InviteToEvent.objects.send_invite(request_user = request_user, invite_user = user, 
                event = event)
        return data

def send_notification_to_subscribe_event_user(*, event: Event, notification_text: str, message_type: str) -> None:
    for user in event.current_users.all():
        send_to_user(user = user, notification_text = f'{user.profile.name},{notification_text}', 
            message_type = message_type, data = {'event_id': event.id})
    for fan in event.current_fans.all():
        send_to_user(user = fan, notification_text = f'{fan.profile.name},{notification_text}', 
            message_type = message_type, data = {'event_id': event.id})

def validate_user_before_join_to_event(*, user: User, event: Event) -> None:
    if user.current_rooms.filter(id = event.id).exists():
        raise ValidationError(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, HTTP_400_BAD_REQUEST)
    if user.current_views_rooms.filter(id = event.id).exists():
        raise ValidationError(ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR, HTTP_400_BAD_REQUEST)
    if event.author.id == user.id:
        raise ValidationError(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, HTTP_400_BAD_REQUEST)
    if RequestToParticipation.objects.filter(user = user,event = event.id, event_author = event.author):
        raise ValidationError(ALREADY_SENT_REQUEST_TO_PARTICIPATE, HTTP_400_BAD_REQUEST)

def send_notification_to_event_author(*, event: Event) -> None:
    if event.amount_members > event.count_current_users:
        user_type: str = 'new'
    elif event.amount_members == event.count_current_users:
        user_type: str = 'last'
    send_to_user(user = User.objects.get(id = event.author.id), notification_text=
        NEW_USER_ON_THE_EVENT_NOTIFICATION.format(author_name = event.author.profile.name, 
        user_type = user_type, event_id = event.id),
        message_type = NEW_USER_ON_THE_EVENT_MESSAGE_TYPE, data = {'event_id': event.id})


def validate_get_user_planned_events(*, pk: int, request_user: User ) -> None:
    user: User = User.objects.get(id = pk)
    if user.configuration['show_my_planned_events'] == False and request_user.id != user.id:
        raise ValidationError(GET_PLANNED_EVENTS_ERROR, HTTP_400_BAD_REQUEST)  


def filter_event_by_user_planned_events_time(*, pk: int, queryset: QuerySet[Event]) -> QuerySet[Event]:
    user: User =  User.objects.get(id = pk)
    num: str = re.findall(r'\d{1,10}', user.get_planned_events)[0]
    string: str = re.findall(r'\D', user.get_planned_events)[0]
    if string == 'd':
        num: int = int(num[0])
    elif string == 'm':  
        num: int = int(num[0]) * 30 + int(num[0]) // 2
    elif string == 'y':
        num: int = int(num[0]) * 365
    finish_date: datetime = timezone.now() + timezone.timedelta(days = int(num))
    return queryset.filter(author_id = user.id, date_and_time__range = [timezone.now(), finish_date])

def only_author(Object):
    def wrap(func: Callable[[Request, int, ...], Response]) -> Callable[[Request, int, ...], Response]:
        def called(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Any:
            try:
                if self.request.user.id == Object.objects.get(id = pk).author.id:
                    return func(self, request, pk, *args, **kwargs)
                raise PermissionDenied()
            except Object.DoesNotExist:
                return Response({'error': f'{json.dumps(Object.__name__)} not found'}, status = HTTP_404_NOT_FOUND)
        return called
    return wrap
