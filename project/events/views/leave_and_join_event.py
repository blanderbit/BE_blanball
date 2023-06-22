# ==============================================================================
# leave_and_join_event.py file which includes all controllers responsible
# for working withremoving the user from the event, sending a request to participate,
# entering and exiting the event for the player and viewer
# ==============================================================================
from typing import Any, Type, final

from authentication.models import User
from chat.tasks import (
    remove_user_from_chat_producer,
)
from drf_yasg.utils import swagger_auto_schema
from events.constants.errors import (
    ALREADY_IN_EVENT_MEMBERS_LIST_ERROR,
    EVENT_AUTHOR_CAN_NOT_JOIN_ERROR,
    NO_IN_EVENT_FANS_LIST_ERROR,
    NO_IN_EVENT_MEMBERS_LIST_ERROR,
)
from events.constants.success import (
    DISCONNECT_FROM_EVENT_SUCCESS,
    JOIN_TO_EVENT_SUCCESS,
    SENT_REQUEST_TO_PARTICIPATION_SUCCESS,
    USER_REMOVED_FROM_EVENT_SUCCESS,
)
from events.models import (
    Event,
    RequestToParticipation,
)
from events.serializers import (
    JoinOrRemoveRoomSerializer,
    RemoveUserFromEventSerializer,
)
from events.services import (
    remove_user_from_event,
    send_message_to_event_author_after_leave_user_from_event,
    send_notification_to_event_author,
    validate_user_before_join_to_event,
)
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)


class JoinToEvent(GenericAPIView):
    """
    Join the event as a member

    This endpoint allows a user who is not the
    author of this event and is not  already on the
    participants or viewers list to enter the event as a participant.
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    @swagger_auto_schema(tags=["event-join"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.objects.get(id=serializer.data["event_id"])
        validate_user_before_join_to_event(user=user, event=event)
        if not event.privacy:
            user.current_rooms.add(event)
            send_notification_to_event_author(event=event, request_user=request.user)
            return Response(JOIN_TO_EVENT_SUCCESS, status=HTTP_200_OK)
        RequestToParticipation.objects.create(
            recipient=event.author, sender=user, event=event
        )
        return Response(SENT_REQUEST_TO_PARTICIPATION_SUCCESS, status=HTTP_200_OK)


class FanJoinToEvent(GenericAPIView):
    """
    Join the event as a spectator

    This endpoint allows a user who is not the
    author of this event and is not  already on the
    participants or viewers list to enter the event as a viewer.
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    @swagger_auto_schema(tags=["event-join"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.objects.get(id=serializer.data["event_id"])
        if event.author.id == request.user.id:
            raise ValidationError(EVENT_AUTHOR_CAN_NOT_JOIN_ERROR, HTTP_400_BAD_REQUEST)
        if not user.current_views_rooms.filter(id=serializer.data["event_id"]).exists():
            user.current_views_rooms.add(event)
            return Response(JOIN_TO_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(
            ALREADY_IN_EVENT_MEMBERS_LIST_ERROR, status=HTTP_400_BAD_REQUEST
        )


class FanLeaveFromEvent(GenericAPIView):
    """
    Leave the event as a spectator

    This endpoint allows the user who is
    at the event as a spectator to leave it
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    @swagger_auto_schema(tags=["event-leave"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.objects.get(id=serializer.data["event_id"])
        if user.current_views_rooms.filter(id=serializer.data["event_id"]).exists():
            user.current_views_rooms.remove(event)
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(NO_IN_EVENT_FANS_LIST_ERROR, status=HTTP_400_BAD_REQUEST)


class LeaveFromEvent(GenericAPIView):
    """
    Leave the event as a member

    This endpoint allows the user who is
    at the event as a participant to leave it
    """

    serializer_class: Type[Serializer] = JoinOrRemoveRoomSerializer

    @swagger_auto_schema(tags=["event-leave"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        event: Event = Event.objects.get(id=serializer.data["event_id"])
        if user.current_rooms.filter(id=serializer.data["event_id"]).exists():
            user.current_rooms.remove(event)
            remove_user_from_chat_producer(user_id=user.id, event_id=event.id)
            send_message_to_event_author_after_leave_user_from_event(
                event=event, user=user
            )
            return Response(DISCONNECT_FROM_EVENT_SUCCESS, status=HTTP_200_OK)
        return Response(NO_IN_EVENT_MEMBERS_LIST_ERROR, status=HTTP_400_BAD_REQUEST)


class RemoveUserFromEvent(GenericAPIView):
    """
    Exclude a user from an event

    This endpoint allows the event author to
    remove (kick) the user from the event for
    one reason or another.
    """

    serializer_class: Type[Serializer] = RemoveUserFromEventSerializer

    @swagger_auto_schema(tags=["events", "event-leave"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        event: Event = Event.objects.get(id=serializer.data["event_id"])
        user: User = User.objects.get(id=serializer.data["user_id"])
        if request.user.id != event.author.id:
            raise PermissionDenied()
        remove_user_from_event(
            user=user, event=event, reason=serializer.validated_data["reason"]
        )
        return Response(USER_REMOVED_FROM_EVENT_SUCCESS, status=HTTP_200_OK)
