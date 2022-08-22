from rest_framework import serializers
from .models import *
from authentication.serializers import UserProfileSerializer


class CreateEventSerializer(serializers.ModelSerializer):
    forms = serializers.ListField(child = serializers.CharField())
    class Meta:
        model = Event
        exclude = ('current_users','author')

    def create(self,validated_data):
        return Event.objects.create(author = self.context['request'].user,**validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DeleteIventsSerializer(serializers.Serializer):
    dele = serializers.ListField(child=serializers.IntegerField(min_value=0))
