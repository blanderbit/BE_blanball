from datetime import datetime
from rest_framework import serializers,status
from .models import *
from project.constaints import *
import pandas
from django.utils import timezone
from authentication.serializers import EventUsersSerializer,EventAuthorSerializer

class CreateUpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('author','current_users','status','fans')

    def validate(self,attrs):
        date_and_time =  attrs.get('date_and_time')
        if date_and_time - timezone.now()+timezone.timedelta(hours=1) > timezone.timedelta(hours=1):
            return super().validate(attrs) 
        raise serializers.ValidationError(BAD_EVENT_TIME_CREATE_ERROR,status.HTTP_400_BAD_REQUEST)
    
    def update(self, instance, validated_data):
        return super().update(instance,validated_data)


class EventSerializer(serializers.ModelSerializer):
    author =  EventAuthorSerializer()
    current_users = EventUsersSerializer(many=True)
    class Meta:
        model = Event
        fields = '__all__'

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('author','id','name','place','amount_members','status','gender',
        'price','type','need_ball','need_form','date_and_time',
        'count_current_users','count_fans') 

class DeleteIventsSerializer(serializers.Serializer):
    event_id = serializers.ListField(child=serializers.IntegerField(min_value=0))


class JoinOrRemoveRoomSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(min_value=0)

    class Meta:
        fields = ('event_id',)

    def validate(self, attrs):
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