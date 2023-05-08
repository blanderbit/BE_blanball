from typing import Type
from scheduler.serializers import (
    UserScheduledEventsSerializer,
)
from scheduler.services import (
    get_user_scheduled_events_data
)
from events.models import (
    Event
)
from django.db.models import (
    QuerySet,
)
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.serializers import (
    Serializer,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class UserScheduledEvents(GenericAPIView):
    """
    User scheduled events

    This endpoint allows the user to 
    get the number of events scheduled by 
    the user for the date range
    """
    serializer_class: Type[Serializer] = UserScheduledEventsSerializer
    queryset: QuerySet[Event] = Event.get_all().filter(status=Event.Status.PLANNED)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        scheduled_events_data = get_user_scheduled_events_data(
            serializer.validated_data,
            self.queryset
        )

        return Response(scheduled_events_data, status=HTTP_200_OK)
