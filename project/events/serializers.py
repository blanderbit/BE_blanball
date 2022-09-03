from datetime import datetime
from rest_framework import serializers,status
from .models import *
from project.constaints import EVENT_NOT_FOUND_ERROR,BAD_EVENT_TIME_CREATE_ERROR
import pandas
from django.utils import timezone

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('author','current_users','status')

    def validate(self,attrs):
        date_and_time =  attrs.get('date_and_time')
        if date_and_time - timezone.now()+timezone.timedelta(hours=1) > timezone.timedelta(hours=1):
            return super().validate(attrs) 
        raise serializers.ValidationError(BAD_EVENT_TIME_CREATE_ERROR,status.HTTP_400_BAD_REQUEST)

    def create(self,validated_data):
        validated_data['date_and_time'] = pandas.to_datetime(validated_data['date_and_time'].isoformat()).round('1min')
        user  = self.context['request'].user
        try:
            if validated_data['contact_number']:
                return Event.objects.create(author = user,**validated_data)
        except:
            return Event.objects.create(author = user, contact_number = User.objects.get(id = user.id).phone,
            **validated_data)

class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('author','current_users','status')

    def validate(self,attrs):
        date_and_time =  attrs.get('date_and_time')
        if date_and_time - timezone.now()+timezone.timedelta(hours=1) > timezone.timedelta(hours=1):
            return super().validate(attrs) 
        raise serializers.ValidationError(BAD_EVENT_TIME_CREATE_ERROR,status.HTTP_400_BAD_REQUEST)



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DeleteIventsSerializer(serializers.Serializer):
    event_id = serializers.ListField(child=serializers.IntegerField(min_value=0))


class JoinOrRemoveRoomSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(min_value=0)

    class Meta:
        fields = ['event_id']

    def validate(self, attrs):
        event_id = attrs.get('event_id')
        event = Event.objects.filter(id = event_id)
        if not event:
            raise serializers.ValidationError(EVENT_NOT_FOUND_ERROR,status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)