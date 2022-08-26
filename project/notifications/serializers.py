from rest_framework import serializers,status
from .models import Notification
from events.models import Event
from project.constaints import EVENT_NOT_FOUND_ERROR


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

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