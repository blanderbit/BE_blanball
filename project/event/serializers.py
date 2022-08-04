from pyexpat import model
from rest_framework import serializers
from .models import *
import datetime


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['author',]

    def create(self,validated_data):
        return EventSerializer.objects.create(author = self.context['request'].author,**validated_data)

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DeleteIventsSerializer(serializers.Serializer):
    dele = serializers.ListField(child=serializers.IntegerField(min_value=0))
