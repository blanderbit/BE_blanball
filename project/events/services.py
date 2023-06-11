import re
from collections import OrderedDict
from datetime import datetime
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    TypeVar,
    Union,
)

import pandas
from authentication.models import User
from config.exceptions import _404
from django.conf import settings
from django.db import transaction
from django.db.models.query import QuerySet
from django.utils import timezone
from events.constants.errors import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,
    ALREADY_SENT_REQUEST_TO_PARTICIPATE_ERROR,
    EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,
    GET_PLANNED_EVENTS_ERROR,
    NO_IN_EVENT_FANS_LIST_ERROR,
)
from events.constants.notification_types import (
    LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_TYPE,
    NEW_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
    RESPONSE_TO_THE_INVITE_TO_EVENT_NOTIFICATION_TYPE,
    RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_NOTIFICATION_TYPE,
    USER_REMOVE_FROM_EVENT_NOTIFICATION_TYPE,
    EVENT_UPDATE_NOTIFICATION_TYPE
)
from events.models import (
    Event,
    InviteToEvent,
    RequestToParticipation,
)
from chat.tasks import edit_chat_producer
from notifications.tasks import send_to_user
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)
from chat.tasks import (
    create_chat_producer,
    add_user_to_chat_producer,
    remove_user_from_chat_producer,
    delete_chat_producer,
)
from utils import (
    generate_unique_request_id
)


bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])


def bulk_delete_events(
    *, data: dict[str, Any], queryset: QuerySet[Event], user: User
) -> bulk:
    for event_id in data:
        try:
            event: Event = queryset.get(id=event_id)
            if event.author == user:
                event.delete()
                delete_chat_producer.delay(
                    event_id=event_id,
                    user_id=user.id
                )
                yield {"success": event_id}
        except Event.DoesNotExist:
            pass


def update_event(*, 
        event: QuerySet[Event], 
        new_data: dict[str, Any], 
        request_user: User
    ) -> None:
    send_notification_to_subscribe_event_user(
        event=event[0], message_type=EVENT_UPDATE_NOTIFICATION_TYPE
    )
    event.update(**new_data)
    edit_chat_producer.delay(
        event_id=event[0].id, 
        user_id=request_user.id,
        new_data=new_data
    )


def bulk_pin_events(
    *, data: dict[str, Any], queryset: QuerySet[Event], user: User
) -> bulk:
    for event_id in data:
        try:
            event: Event = queryset.get(id=event_id)
            if (
                event.author == user
                and user.count_pinned_events < settings.MAX_COUNT_PINNED_EVENTS
            ):
                event.pinned = True
                event.save()
                yield {"success": event_id}
        except Event.DoesNotExist:
            pass


def bulk_show_or_hide_events(
    *, data: dict[str, Any], queryset: QuerySet[Event], user: User
) -> bulk:
    for event_id in data:
        try:
            event: Event = queryset.get(id=event_id)
            if (
                user in event.current_users.all() or
                user in event.current_fans.all()
                and event.status == Event.Status.PLANNED
            ):
                event.hidden = not event.hidden
                event.save()
                yield {"success": event_id}
        except Event.DoesNotExist:
            pass


def bulk_unpin_events(
    *, data: dict[str, Any], queryset: QuerySet[Event], user: User
) -> bulk:
    for event_id in data:
        try:
            event: Event = queryset.get(id=event_id)
            if event.author == user:
                event.pinned = False
                event.save()
                yield {"success": event_id}
        except Event.DoesNotExist:
            pass


def send_message_after_bulk_accept_or_decline(
    *,
    object: Union[RequestToParticipation, InviteToEvent],
    message_type: str,
    response: bool,
) -> None:
    if isinstance(object, RequestToParticipation):
        message_obejct_name: str = "request"
    if isinstance(object, InviteToEvent):
        message_obejct_name: str = "invite"
    send_to_user(
        user=object.sender,
        message_type=message_type,
        data={
            "recipient": {
                "id": object.sender.id,
                "name": object.sender.profile.name,
                "last_name": object.sender.profile.last_name,
            },
            "event": {
                "id": object.event.id,
                "name": object.event.name,
            },
            message_obejct_name: {
                "id": object.id,
                "response": response,
            },
            "sender": {
                "id": object.recipient.id,
                "name": object.recipient.profile.name,
                "last_name": object.recipient.profile.last_name,
            },
        },
    )


def bulk_accept_or_decline_invites_to_events(
    *, data: dict[str, Union[list[int], bool]], request_user: User
) -> bulk:
    for invite_id in data["ids"]:
        try:
            invite: InviteToEvent = InviteToEvent.objects.get(id=invite_id)
            if (
                invite.recipient.id == request_user.id
                and invite.status == invite.Status.WAITING
            ):
                if invite.event.current_users.count() < invite.event.amount_members:
                    if data["type"] == True:
                        invite.status = invite.Status.ACCEPTED
                        add_user_to_chat_producer.delay(
                            user_id=invite.recipient.id,
                            event_id=invite.event.id
                        )
                        invite.recipient.current_rooms.add(invite.event)
                    else:
                        invite.status = invite.Status.DECLINED
                    invite.save()
                    send_message_after_bulk_accept_or_decline(
                        object=invite,
                        message_type=RESPONSE_TO_THE_INVITE_TO_EVENT_NOTIFICATION_TYPE,
                        response=data["type"],
                    )
                    yield {"success": invite_id}

        except InviteToEvent.DoesNotExist:
            pass


def bulk_accpet_or_decline_requests_to_participation(
    *, data: dict[str, Union[list[int], bool]], request_user: User
) -> bulk:
    for request_id in data["ids"]:
        try:
            request_to_p: RequestToParticipation = RequestToParticipation.objects.get(
                id=request_id
            )
            if (
                request_to_p.recipient.id == request_user.id
                and request_to_p.status == request_to_p.Status.WAITING
            ):
                if data["type"] == True:
                    if (
                        request_to_p.event.current_users.count()
                        < request_to_p.event.amount_members
                    ):
                        request_to_p.status = request_to_p.Status.ACCEPTED
                        request_to_p.sender.current_rooms.add(request_to_p.event)
                        add_user_to_chat_producer.delay(
                            user_id=request_to_p.sender.id,
                            event_id=request_to_p.event.id
                        )
                else:
                    request_to_p.status = request_to_p.Status.DECLINED
                request_to_p.save()
                send_message_after_bulk_accept_or_decline(
                    object=request_to_p,
                    message_type=RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_NOTIFICATION_TYPE,
                    response=data["type"],
                )
                yield {"success": request_id}
        except RequestToParticipation.DoesNotExist:
            pass


def create_event_chat(*,
                      event: Event,
                      request_user: User
                      ) -> None:
    event_players_chat_data = {
        "author": request_user.id,
        "name": f"{event.date_and_time}/{event.name}",
        "users": [],
        "type": "Event_Group",
        "event_id": event.id
    }

    create_chat_producer.delay(
        data=event_players_chat_data,
        author_id=request_user.id,
        request_id=generate_unique_request_id()
    )


def event_create(
    *, data: Union[dict[str, Any], OrderedDict[str, Any]], request_user: User
) -> dict[str, Any]:
    data = dict(data)
    users: list[User] = data["current_users"]
    data.pop("current_users")
    try:
        contact_number: str = data["contact_number"]
    except KeyError:
        contact_number: str = str(User.objects.get(id=request_user.id).phone)
    data["contact_number"] = contact_number
    data["date_and_time"] = (
        pandas.to_datetime(data["date_and_time"].isoformat())
        .round("1min")
        .to_pydatetime()
    )
    with transaction.atomic():
        event: Event = Event.objects.create(**data, author=request_user)
        for user in users:
            InviteToEvent.objects.send_invite(
                request_user=request_user, invite_user=user, event=event
            )
        create_event_chat(event=event, request_user=request_user)
        return data


def send_notification_to_subscribe_event_user(
    *,
    event: Event,
    message_type: str,
    start_time: datetime = None,
    time_to_start: int = None,
) -> None:
    for user in list(event.current_users.all()) + list(event.current_fans.all()):
        send_to_user(
            user=user,
            message_type=message_type,
            data={
                "sender": {
                    "id": event.author.id,
                    "name": event.author.profile.name,
                    "last_name": event.author.profile.last_name,
                },
                "recipient": {
                    "id": user.id,
                    "name": user.profile.name,
                    "last_name": user.profile.last_name,
                },
                "event": {
                    "id": event.id,
                    "start_time": start_time,
                    "time_to_start": time_to_start,
                },
            },
        )


def validate_user_before_join_to_event(*, user: User, event: Event) -> None:
    if user.current_rooms.filter(id=event.id).exists():
        raise ValidationError(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, HTTP_400_BAD_REQUEST)
    if user.current_views_rooms.filter(id=event.id).exists():
        raise ValidationError(NO_IN_EVENT_FANS_LIST_ERROR, HTTP_400_BAD_REQUEST)
    if event.author.id == user.id:
        raise ValidationError(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, HTTP_400_BAD_REQUEST)
    if user in event.black_list.all():
        raise PermissionDenied()
    if RequestToParticipation.get_all().filter(
        sender=user, event=event.id, recipient=event.author
    ):
        raise ValidationError(
            ALREADY_SENT_REQUEST_TO_PARTICIPATE_ERROR, HTTP_400_BAD_REQUEST
        )


def send_notification_to_event_author(*, event: Event, request_user: User) -> None:
    send_to_user(
        user=User.objects.get(id=event.author.id),
        message_type=NEW_USER_ON_THE_EVENT_NOTIFICATION_TYPE,
        data={
            "recipient": {
                "id": event.author.id,
                "name": event.author.profile.name,
                "last_name": event.author.profile.last_name,
            },
            "event": {
                "id": event.id,
                "name": event.name,
            },
            "sender": {
                "id": request_user.id,
                "name": request_user.profile.name,
                "last_name": request_user.profile.last_name,
            },
        },
    )


def validate_get_user_planned_events(*, pk: int, request_user: User) -> None:
    user: User = User.objects.get(id=pk)
    if (
        user.configuration["show_my_planned_events"] == False
        and request_user.id != user.id
    ):
        raise ValidationError(GET_PLANNED_EVENTS_ERROR, HTTP_400_BAD_REQUEST)


def filter_event_by_user_planned_events_time(
    *, pk: int, queryset: QuerySet[Event]
) -> QuerySet[Event]:
    user: User = User.objects.get(id=pk)
    num: str = re.findall(r"\d{1,10}", user.get_planned_events)[0]
    string: str = re.findall(r"\D", user.get_planned_events)[0]
    if string == "d":
        num: int = int(num[0])
    elif string == "m":
        num: int = int(num[0]) * 30 + int(num[0]) // 2
    elif string == "y":
        num: int = int(num[0]) * 365
    finish_date: datetime = timezone.now() + timezone.timedelta(days=int(num))
    return queryset.filter(
        author_id=user.id, date_and_time__range=[timezone.now(), finish_date]
    )


def only_author(Object):
    def wrap(
        func: Callable[[Request, int, ...], Response]
    ) -> Callable[[Request, int, ...], Response]:
        def called(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Any:
            try:
                if self.request.user.id == Object.objects.get(id=pk).author.id:
                    return func(self, request, pk, *args, **kwargs)
                raise PermissionDenied()
            except Object.DoesNotExist:
                raise _404(object=Object)

        return called

    return wrap


def not_in_black_list(
    func: Callable[[Request, int, ...], Response]
) -> Callable[[Request, int, ...], Response]:
    def wrap(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Any:
        try:
            if request.user in Event.objects.get(id=pk).black_list.all():
                raise PermissionDenied()
            return func(self, request, pk, *args, **kwargs)
        except Event.DoesNotExist:
            raise _404(object=Event)

    return wrap


def remove_user_from_event(*, user: User, event: Event, reason: str) -> None:
    user.current_rooms.remove(event)
    remove_user_from_chat_producer.delay(
        user_id=user.id,
        event_id=event.id
    )
    event.black_list.add(user)
    send_to_user(
        user=user,
        message_type=USER_REMOVE_FROM_EVENT_NOTIFICATION_TYPE,
        data={
            "recipient": {
                "id": user.id,
                "name": user.profile.name,
                "last_name": user.profile.last_name,
            },
            "reason": {"text": reason},
            "event": {
                "id": event.id,
                "name": event.name,
            },
        },
    )


def only_for_event_members(func):
    def wrap(self, request: Request, *agrs: Any, **kwargs: Any):
        try:
            event: Event = Event.objects.get(id=request.data["event"])
            if request.user in event.current_users.all():
                return func(self, request, *agrs, **kwargs)
            else:
                raise PermissionDenied()
        except Event.DoesNotExist:
            return func(self, request, *agrs, **kwargs)

    return wrap


def send_message_to_event_author_after_leave_user_from_event(
    *, event: Event, user: User
) -> None:
    send_to_user(
        user=event.author,
        message_type=LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_TYPE,
        data={
            "recipient": {
                "id": event.author.id,
                "name": event.author.profile.name,
                "last_name": event.author.profile.last_name,
            },
            "event": {
                "id": event.id,
                "name": event.name,
            },
            "sender": {
                "id": user.id,
                "name": user.profile.name,
                "last_name": user.profile.last_name,
            },
        },
    )


def invite_users_to_event(*, event_id: int, users_ids: list[int], request_user: User) -> None:
    event: Event = Event.objects.get(id=event_id)

    for user_id in users_ids:
        invite_user: User = User.objects.get(id=user_id)

        try:
            InviteToEvent.objects.send_invite(
                request_user=request_user, invite_user=invite_user, event=event
            )
            yield {"success": invite_user.id}
        except ValidationError:
            pass
