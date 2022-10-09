import re

from django.utils import timezone
from django.db.models.query import QuerySet

from rest_framework.serializers import ValidationError,Serializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)

from authentication.models import User
from events.models import (
    Event,
    RequestToParticipation,
)
from events.constaints import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR, EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, 
    ALREADY_SENT_REQUEST_TO_PARTICIPATE, NEW_USER_ON_THE_EVENT_NOTIFICATION, NEW_USER_ON_THE_EVENT_MESSAGE_TYPE,
    RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION, RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE
)
from notifications.tasks import send_to_user

def send_notification_to_subscribe_event_user(event: Event, notification_text: str, message_type: str) -> None:
    for user in event.current_users.all():
        send_to_user(user = user, notification_text = f'{user.profile.name},{notification_text}', 
            message_type = message_type)
    for fan in event.fans.all():
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


def bulk_delete_events(serializer: Serializer, queryset: QuerySet, user: User) -> dict[str, list[int]]:
    deleted: list[int] = [] 
    not_deleted: list[int] = []
    for event_id in serializer.validated_data['events']:
        event: Event = queryset.filter(id = event_id)
        if event:
            event = queryset.get(id = event_id)
            if event.author == user:
                event.delete()
                deleted.append(event_id)
            else:
                not_deleted.append(event_id)
        else:
            not_deleted.append(event_id)
    return {'delete success': deleted, 'delete error':  not_deleted}

def bulk_accpet_or_decline(serializer: Serializer,queryset: QuerySet,user: User) -> dict[str,list[int]]:
    success: list[int] = []
    not_success: list[int] = []
    for request_id in serializer.validated_data['requests']:
        request_to_p = queryset.filter(id = request_id)
        if request_to_p:
            request_to_p = queryset.get(id = request_id)
            if request_to_p.event_author.id == user.id:
                if serializer.validated_data['type'] == True:
                    send_to_user(user = request_to_p.user, notification_text = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION.format(
                        user_name = request_to_p.user.profile.name, event_id = request_to_p.event.id, response_type = 'accepted'),
                        message_type = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                    success.append(request_id)
                    request_to_p.user.current_rooms.add(request_to_p.event)
                    request_to_p.delete()
                else:
                    send_to_user(user = request_to_p.user, notification_text = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION.format(
                        user_name = request_to_p.user.profile.name,event_id = request_to_p.event.id,response_type = 'rejected'),
                        message_type = RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE)
                    success.append(request_id)
                    request_to_p.delete()
            else:
                not_success.append(request_id)
        else:
            not_success.append(request_id)
    return {"success": success, "error":  not_success}

