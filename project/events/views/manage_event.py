from typing import Any, Type, final

from config.serializers import (
    BaseBulkSerializer,
)
from django.db.models.query import QuerySet
from events.constants.success import (
    EVENT_UPDATE_SUCCESS,
)
from events.models import Event
from events.serializers import (
    CreateEventSerializer,
    EventSerializer,
    UpdateEventSerializer,
)
from events.services import (
    bulk_delete_events,
    bulk_pin_events,
    bulk_unpin_events,
    event_create,
    not_in_black_list,
    only_author,
    update_event,
    bulk_show_or_hide_events,
)
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    RetrieveModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)


class CreateEvent(GenericAPIView):
    """
    Event create

    This endpoint allows the user to create an event.
    The user can also specify the ID of other users in
    the current_users field to send them invitations.

    privacy true - means that it will not be possible
    to simply connect to the event, everything will go
    through the rejection or acceptance of applications
    by the author of the event.

    privacy false - means that the event has open access
    and anyone can connect to it.

    gender field options: Man, Wooman
    type field options: Football, Futsal
    forms field options: Shirt-Front, T-Shirt, Any
    duration field options: 10, 20, 30, 40, 50, 60, 70,
    80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180",
    """

    serializer_class: Type[Serializer] = CreateEventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, Any] = event_create(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_201_CREATED)


class UpdateEvent(GenericAPIView):
    """
    Update event

    This endpoint allows the event author
    to change any data on the event
    """

    serializer_class: Type[Serializer] = UpdateEventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    @only_author(Event)
    def put(self, request: Request, pk: int) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_event(
            event=self.queryset.filter(id=pk),
            new_data=serializer.validated_data,
            request_user=request.user
        )
        return Response(EVENT_UPDATE_SUCCESS, status=HTTP_200_OK)


class DeleteEvents(GenericAPIView):
    """
    Delete event

    This endpoint allows the user to delete
    their events.If the user deletes the event,
    it can no longer be restored.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_delete_events(
            data=serializer.validated_data["ids"],
            queryset=self.queryset,
            user=request.user,
        )
        return Response(data, status=HTTP_200_OK)


class PinMyEvents(GenericAPIView):
    """
    Pin my events

    This endpoint allows the user to pin
    their events.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_pin_events(
            data=serializer.validated_data["ids"],
            queryset=self.queryset,
            user=request.user,
        )
        return Response(data, status=HTTP_200_OK)


class ShowOrHideMyEvents(GenericAPIView):
    """
    Show or hide my events

    This endpoint allows the user to show or hide
    their events.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_show_or_hide_events(
            data=serializer.validated_data["ids"],
            queryset=self.queryset,
            user=request.user,
        )
        return Response(data, status=HTTP_200_OK)


class UnPinMyEvents(GenericAPIView):
    """
    UnPin my events

    This endpoint allows the user to unpin
    their events.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    queryset: QuerySet[Event] = Event.get_all()

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_unpin_events(
            data=serializer.validated_data["ids"],
            queryset=self.queryset,
            user=request.user,
        )
        return Response(data, status=HTTP_200_OK)


class GetEvent(RetrieveModelMixin, GenericAPIView):
    """
    Get event

    This endpoint allows the user, with the exception
    of those blacklisted for this event,
    get detailed information about any event.
    """

    serializer_class: Type[Serializer] = EventSerializer
    queryset: QuerySet[Event] = Event.get_all()

    @not_in_black_list
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MyPinnedEventsCount(GenericAPIView):
    def get(self, request):
        return Response({"count": request.user.count_pinned_events}, status=HTTP_200_OK)
