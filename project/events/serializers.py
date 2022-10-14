from keyword import kwlist
from events.models import (
    Event,
    EventTemplate,
    RequestToParticipation,
)
from authentication.serializers import EventUsersSerializer

from collections import OrderedDict

from rest_framework import serializers

from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)

from events.validators import EventDateTimeValidator

from events.constaints import (
    EVENT_TIME_EXPIRED_ERROR, NO_EVENT_PLACE_ERROR, EVENT_NOT_FOUND_ERROR, AUTHOR_CAN_NOT_INVITE_ERROR,
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, ALREADY_IN_EVENT_FANS_LIST_ERROR, 
)
from authentication.constaints import (
    NO_SUCH_USER_ERROR,
)

from authentication.models import User

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = (
            'author',
            'status',
            'current_fans',
        )


class TemplateCreateSerializer(serializers.ModelSerializer):
    event_data = CreateEventSerializer()

    class Meta:
        model = EventTemplate
        exclude = (
            'author',
        )

class TemplateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTemplate
        exclude = (
            'author',
        )

class EventTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = (
            'author',
            'status',
            'current_fans',
            'current_users',
            'description',
        )

class TemplateListSerializer(serializers.ModelSerializer):
    event_data = EventTemplateListSerializer()
    class Meta:
        model = EventTemplate
        fields = (
            'id',
            'name', 
            'time_created', 
            'count_current_users', 
            'event_data',
        )


class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = (
            'author',
            'status',
            'current_fans',
            'current_users',
        )

    def update(self, instance, validated_data: dict) -> OrderedDict:
        return super().update(instance, validated_data)

class EventSerializer(serializers.ModelSerializer):
    author =  EventUsersSerializer()
    current_users = EventUsersSerializer(many=True)
    class Meta:
        model = Event
        fields = '__all__'

class PopularIventsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'author',
            'id',
            'name',
            'place',
            'gender',
            'date_and_time',
            'type',
        )    

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'author',
            'id',
            'name',
            'place',
            'amount_members',
            'status',
            'gender',
            'price',
            'type',
            'need_ball',
            'duration',
            'need_form',
            'privacy',
            'date_and_time',
            'count_current_users',
            'count_current_fans',
        ) 

class DeleteIventsSerializer(serializers.Serializer):
    ids: list[int] = serializers.ListField(child = serializers.IntegerField(min_value = 0))

    class Meta:
        fieds = ('ids', )


class JoinOrRemoveRoomSerializer(serializers.Serializer):
    event_id: int = serializers.IntegerField(min_value = 0)

    class Meta:
        fields = ('event_id', )

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        event_id: int = attrs.get('event_id')
        try:
            event: Event = Event.objects.get(id = event_id)
            if event.status != 'Planned':
                raise serializers.ValidationError(EVENT_TIME_EXPIRED_ERROR, HTTP_400_BAD_REQUEST)
            if event.amount_members < event.count_current_users + 1:
                raise serializers.ValidationError(NO_EVENT_PLACE_ERROR, HTTP_400_BAD_REQUEST)
            return super().validate(attrs)
        except Event.DoesNotExist:
            raise serializers.ValidationError(EVENT_NOT_FOUND_ERROR, HTTP_404_NOT_FOUND)

class InviteUserToEventSerializer(serializers.Serializer):
    user_id: int = serializers.IntegerField(min_value = 0)
    event_id: int = serializers.IntegerField(min_value = 0)

    class Meta:
        fields = (
            'event_id',
            'user_id',
        )

    def validate(self, attrs) -> OrderedDict:
        try:
            invite_user = User.objects.get(id = attrs.get('user_id'))
            event = Event.objects.get(id = attrs.get('event_id'))
            if event.status == 'Finished':
                raise serializers.ValidationError(EVENT_TIME_EXPIRED_ERROR, HTTP_400_BAD_REQUEST)
            if invite_user.id == Event.objects.get(id = event.id).author.id:
                raise serializers.ValidationError(AUTHOR_CAN_NOT_INVITE_ERROR , HTTP_400_BAD_REQUEST)
            if invite_user.current_rooms.filter(id = event.id).exists():
                raise serializers.ValidationError(ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, HTTP_400_BAD_REQUEST)
            if invite_user.current_views_rooms.filter(id = event.id).exists():
                raise serializers.ValidationError(ALREADY_IN_EVENT_FANS_LIST_ERROR, HTTP_400_BAD_REQUEST)
            return super().validate(attrs)
        except User.DoesNotExist:
            raise serializers.ValidationError(NO_SUCH_USER_ERROR, HTTP_404_NOT_FOUND)
        except Event.DoesNotExist:
            raise serializers.ValidationError(EVENT_NOT_FOUND_ERROR, status = HTTP_404_NOT_FOUND)


class RequestToParticipationSerializer(serializers.ModelSerializer):
    user = EventUsersSerializer()
    class Meta:
        model = RequestToParticipation
        fields = (
            'id',
            'user',
            'time_created',
        )

class BulkAcceptOrDeclineRequestToParticipationSerializer(serializers.Serializer):
    requests: list[int] = serializers.ListField(child=serializers.IntegerField(min_value = 0))
    type: bool = serializers.BooleanField()

    class Meta:
        fields = (
            'requests',
            'type',
        )

