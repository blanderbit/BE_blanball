from rest_framework import serializers
from .models import *
import datetime


class EventSerializer(serializers.ModelSerializer):
    serializers.ListField(child=serializers.IntegerField(min_value=0))
    class Meta:
        model = Event
        fields = '__all__'

class DeleteIventsSerializer(serializers.Serializer):
    dele = serializers.ListField(child=serializers.IntegerField(min_value=0))
