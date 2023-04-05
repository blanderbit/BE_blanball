from collections import OrderedDict
from typing import Any, Union

from authentication.models import User
from authentication.serializers import (
    EventAuthorSerializer,
    EventUsersSerializer,
)
from cities.serializers import PlaceSerializer
from config.exceptions import _404
from config.serializers import (
    BaseBulkSerializer,
)
from events.constants.errors import (
    ALREADY_IN_EVENT_FANS_LIST_ERROR,
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,
    EVENT_TIME_EXPIRED_ERROR,
    NO_EVENT_PLACE_ERROR,
    NO_IN_EVENT_MEMBERS_LIST_ERROR,
)
from events.models import (
    Event,
    InviteToEvent,
    RequestToParticipation,
)
from events.validators import (
    EventDateTimeValidator,
)
from rest_framework.serializers import (
    BooleanField,
    CharField,
    ChoiceField,
    IntegerField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


class CreateEventSerializer(ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model: Event = Event
        validators = [EventDateTimeValidator()]
        exclude: Union[str, list[str]] = [
            "author",
            "status",
            "current_fans",
            "black_list",
            "coordinates",
            "pinned",
        ]


class UpdateEventSerializer(ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model: Event = Event
        exclude: Union[str, list[str]] = [
            "author",
            "status",
            "current_fans",
            "current_users",
            "black_list",
            "coordinates",
            "pinned",
        ]

    def update(self, instance, validated_data: dict) -> OrderedDict:
        return super().update(instance, validated_data)


class EventSerializer(ModelSerializer):
    author = EventAuthorSerializer()
    current_users = EventUsersSerializer(many=True)
    current_fans = EventUsersSerializer(many=True)

    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "id",
            "author",
            "name",
            "description",
            "gender",
            "date_and_time",
            "contact_number",
            "need_ball",
            "amount_members",
            "type",
            "price",
            "price_description",
            "need_form",
            "status",
            "privacy",
            "duration",
            "forms",
            "request_user_role",
            "place",
            "coordinates",
            "current_users",
            "current_fans",
        ]


class PopularEventsListSerializer(ModelSerializer):
    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "author",
            "id",
            "name",
            "place",
            "gender",
            "date_and_time",
            "type",
        ]


class EventListSerializer(ModelSerializer):
    place = PlaceSerializer()
    author = EventAuthorSerializer()

    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "id",
            "author",
            "name",
            "place",
            "amount_members",
            "status",
            "gender",
            "description",
            "price",
            "type",
            "need_ball",
            "forms",
            "duration",
            "need_form",
            "privacy",
            "date_and_time",
            "count_current_users",
            "count_current_fans",
            "request_user_role",
        ]

    def to_representation(self, instance):
        try:
            event_id = instance.id
            user_id = self.context.get("request").parser_context["kwargs"]["pk"]
            event = Event.objects.get(id=event_id)
            data = super().to_representation(instance)
            data["pk_user_role"] = event.get_user_role(pk=user_id)
            return data
        except KeyError:
            data = super().to_representation(instance)
            return data


class MyEventListSerializer(ModelSerializer):
    place = PlaceSerializer()
    author = EventAuthorSerializer()

    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "id",
            "author",
            "name",
            "place",
            "amount_members",
            "status",
            "gender",
            "description",
            "price",
            "type",
            "need_ball",
            "pinned",
            "forms",
            "duration",
            "need_form",
            "privacy",
            "date_and_time",
            "count_current_users",
            "count_current_fans",
            "request_user_role",
        ]


class InInvitesEventSerializer(ModelSerializer):
    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "date_and_time",
        ]


class InvitesToEventListSerializer(ModelSerializer):
    event = InInvitesEventSerializer()
    sender = EventUsersSerializer()

    class Meta:
        model: InviteToEvent = InviteToEvent
        fields: Union[str, list[str]] = [
            "id",
            "time_created",
            "event",
            "sender",
        ]


class JoinOrRemoveRoomSerializer(Serializer):
    event_id: int = IntegerField(min_value=0)

    class Meta:
        fields: Union[str, list[str]] = [
            "event_id",
        ]

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        event_id: int = attrs.get("event_id")
        try:
            event: Event = Event.get_all().get(id=event_id)
            if event.status != event.Status.PLANNED:
                raise ValidationError(EVENT_TIME_EXPIRED_ERROR, HTTP_400_BAD_REQUEST)
            if event.amount_members < event.count_current_users + 1:
                raise ValidationError(NO_EVENT_PLACE_ERROR, HTTP_400_BAD_REQUEST)
            return super().validate(attrs)
        except Event.DoesNotExist:
            raise _404(object=Event)


class InviteUsersToEventSerializer(Serializer):
    user_id: int = IntegerField(min_value=0)
    event_id: int = IntegerField(min_value=0)

    class Meta:
        fields: Union[str, list[str]] = [
            "event_id",
            "user_id",
        ]

    def validate(self, attrs) -> OrderedDict[str, Any]:
        try:
            invite_user: User = User.get_all().get(id=attrs.get("user_id"))
            event: Event = Event.get_all().get(id=attrs.get("event_id"))
            if event.status == Event.Status.FINISHED:
                raise ValidationError(EVENT_TIME_EXPIRED_ERROR, HTTP_400_BAD_REQUEST)
            if invite_user.current_rooms.filter(id=event.id).exists():
                raise ValidationError(
                    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, HTTP_400_BAD_REQUEST
                )
            if invite_user.current_views_rooms.filter(id=event.id).exists():
                raise ValidationError(
                    ALREADY_IN_EVENT_FANS_LIST_ERROR, HTTP_400_BAD_REQUEST
                )
            return super().validate(attrs)
        except User.DoesNotExist:
            raise _404(object=User)
        except Event.DoesNotExist:
            raise _404(object=Event)


class RemoveUserFromEventSerializer(Serializer):
    user_id: int = IntegerField(min_value=0)
    event_id: int = IntegerField(min_value=0)
    reason: str = CharField(max_length=255)

    class Meta:
        fields: Union[str, list[str]] = [
            "event_id",
            "user_id",
            "reason",
        ]

    def validate(self, attrs) -> OrderedDict[str, Any]:
        try:
            removed_user: User = User.get_all().get(id=attrs.get("user_id"))
            event: Event = Event.get_all().get(id=attrs.get("event_id"))
            if event.status == event.Status.FINISHED:
                raise ValidationError(EVENT_TIME_EXPIRED_ERROR, HTTP_400_BAD_REQUEST)
            if not removed_user.current_rooms.filter(id=event.id).exists():
                raise ValidationError(
                    NO_IN_EVENT_MEMBERS_LIST_ERROR, HTTP_400_BAD_REQUEST
                )
            return super().validate(attrs)
        except User.DoesNotExist:
            raise _404(object=User)
        except Event.DoesNotExist:
            raise _404(object=Event)


class RequestToParticipationSerializer(ModelSerializer):
    sender = EventUsersSerializer()
    event = InInvitesEventSerializer()

    class Meta:
        model: RequestToParticipation = RequestToParticipation
        fields: Union[str, list[str]] = "__all__"


class BulkAcceptOrDeclineRequestToParticipationSerializer(BaseBulkSerializer):
    type: bool = BooleanField()

    class Meta:
        fields: Union[str, list[str]] = [
            "type",
        ]
