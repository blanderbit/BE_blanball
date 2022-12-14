from .models import *
from project.constaints import *
from authentication.serializers import EventUsersSerializer
from authentication.models import User

from collections import OrderedDict

from django.utils import timezone

from rest_framework import serializers,status


class EventDateTimeValidator:

    def __call__(self,attrs) -> OrderedDict:
        date_and_time =  attrs.get('date_and_time')
        price = attrs.get('price')
        price_desc = attrs.get('price_description')
        if date_and_time - timezone.now()+timezone.timedelta(hours=1) < timezone.timedelta(hours=1):
            raise serializers.ValidationError(BAD_EVENT_TIME_CREATE_ERROR,status.HTTP_400_BAD_REQUEST)
        if price and price > 0 and price_desc == None:
            raise serializers.ValidationError(NO_PRICE_DESK_ERROR,status.HTTP_400_BAD_REQUEST)
        if not price and price_desc:
            raise serializers.ValidationError(NO_PRICE_DESK_ERROR,status.HTTP_400_BAD_REQUEST)
        return attrs

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = ('author','status','fans')


class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        validators = [EventDateTimeValidator()]
        exclude = ('author','status','fans','current_users')

    def update(self, instance, validated_data) -> OrderedDict:
        return super().update(instance,validated_data)

class EventSerializer(serializers.ModelSerializer):
    author =  EventUsersSerializer()
    current_users = EventUsersSerializer(many=True)
    class Meta:
        model = Event
        fields = '__all__'

class PopularIventsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('author','id','name','place','gender','date_and_time','type')    

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('author','id','name','place','amount_members','status','gender',
        'price','type','need_ball','need_form','date_and_time',
        'count_current_users','count_fans') 

class DeleteIventsSerializer(serializers.Serializer):
    events = serializers.ListField(child=serializers.IntegerField(min_value=0))


class JoinOrRemoveRoomSerializer(serializers.Serializer):
    event_id:int = serializers.IntegerField(min_value=0)

    class Meta:
        fields = ('event_id',)

    def validate(self, attrs) -> OrderedDict:
        event_id = attrs.get('event_id')
        try:
            event = Event.objects.get(id = event_id)
            if event.status != 'Planned':
                raise serializers.ValidationError(EVENT_TIME_EXPIRED_ERROR ,status.HTTP_400_BAD_REQUEST)
            if event.amount_members < event.count_current_users+1:
                raise serializers.ValidationError(NO_EVENT_PLACE_ERROR,status.HTTP_400_BAD_REQUEST)
            return super().validate(attrs)
        except Event.DoesNotExist:
            raise serializers.ValidationError(EVENT_NOT_FOUND_ERROR,status.HTTP_404_NOT_FOUND)


class InviteUserToEventSerializer(serializers.Serializer):
    user_id:User.id = serializers.IntegerField(min_value=0)
    event_id:Event.id = serializers.IntegerField(min_value=0)

    class Meta:
        fields = ('event_id','user_id')


class RequestToParticipationSerializer(serializers.ModelSerializer):
    user = EventUsersSerializer()
    class Meta:
        model = RequestToParticipation
        fields = ('id','user','time_created')

class BulkAcceptOrDeclineRequestToParticipationSerializer(serializers.Serializer):
    requests = serializers.ListField(child=serializers.IntegerField(min_value=0))
    type = serializers.BooleanField()

    class Meta:
        fields = ('requests','type')

