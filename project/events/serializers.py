from events.models import (
    Event,
    RequestToParticipation,
)
from project.constaints import *
from authentication.serializers import EventUsersSerializer

from collections import OrderedDict

from rest_framework import serializers

from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)

from events.validators import EventDateTimeValidator


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = (
            'author',
            'status',
            'fans',
        )

class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = (
            'author',
            'status',
            'fans',
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
            'need_form',
            'date_and_time',
            'count_current_users',
            'count_fans',
        ) 

class DeleteIventsSerializer(serializers.Serializer):
    events: list[int] = serializers.ListField(child = serializers.IntegerField(min_value = 0))


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

