from scheduler.constants.errors import (
    SCHEDULER_FINISH_DATE_LESS_THAN_START_DATE,
)
from typing import Any, Union

from rest_framework.serializers import (
    Serializer,
    DateField,
    ValidationError,
    IntegerField
)

from rest_framework.status import (
    HTTP_400_BAD_REQUEST
)


class UserScheduledEventsSerializer(Serializer):

    user_id = IntegerField(min_value=0)
    start_date = DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    finish_date = DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        fields: Union[str, list[str]] = [
            "user_id",
            "start_date",
            "finish_date"
        ]

    def validate(self, data):
        if data["finish_date"] < data["start_date"]:
            raise ValidationError(
                SCHEDULER_FINISH_DATE_LESS_THAN_START_DATE, HTTP_400_BAD_REQUEST
            )
        return data
