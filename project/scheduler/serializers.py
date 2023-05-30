from scheduler.constants.errors import (
    SCHEDULER_FINISH_DATE_LESS_THAN_START_DATE,
)
from events.serializers import PlaceSerializer
from events.serializers import EventAuthorSerializer, EventUsersSerializer
from events.models import Event
from typing import Any, Union

from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    DateField,
    ValidationError,
    IntegerField,
)

from rest_framework.status import HTTP_400_BAD_REQUEST


class UserScheduledEventsSerializer(Serializer):

    user_id = IntegerField(min_value=0)
    start_date = DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    finish_date = DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        fields: Union[str, list[str]] = ["user_id", "start_date", "finish_date"]

    def validate(self, data):
        if data["finish_date"] < data["start_date"]:
            raise ValidationError(
                SCHEDULER_FINISH_DATE_LESS_THAN_START_DATE, HTTP_400_BAD_REQUEST
            )
        return data


class ListOfUserScheduledEventsOnSpecificDaySerializer(ModelSerializer):
    place = PlaceSerializer()
    author = EventAuthorSerializer()
    current_users = EventUsersSerializer(many=True)

    class Meta:
        model: Event = Event
        fields: Union[str, list[str]] = [
            "id",
            "author",
            "name",
            "price",
            "date_and_time",
            "duration",
            "amount_members",
            "place",
            "type",
            "status",
            "request_user_role",
            "current_users",
        ]
