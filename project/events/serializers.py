from datetime import datetime
from rest_framework import serializers,status
from .models import *
from project.constaints import EVENT_NOT_FOUND_ERROR
import pandas

class EventSerializer(serializers.ModelSerializer):
    forms = serializers.ListField(child = serializers.CharField())
    class Meta:
        model = Event
        exclude = ('current_users','author')

    def create(self,validated_data):
        validated_data['date_and_time'] = pandas.to_datetime(validated_data['date_and_time'].isoformat()).round('1min')
        return Event.objects.create(author = self.context['request'].user,**validated_data)
    


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DeleteIventsSerializer(serializers.Serializer):
    dele = serializers.ListField(child=serializers.IntegerField(min_value=0))


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