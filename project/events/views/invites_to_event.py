# ==============================================================================
# events_list.py file which includes all controllers responsible for working with
# requests for participation in the event and invitations to events
# ==============================================================================

from typing import Any, Type, final

from authentication.models import User
from config.exceptions import _404
from config.openapi import (
    offset_query,
    skip_param_query,
)
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from events.decorators import not_in_black_list
from events.models import (
    Event,
    InviteToEvent,
    RequestToParticipation,
)
from events.serializers import (
    BulkAcceptOrDeclineRequestToParticipationSerializer,
    InvitesToEventListSerializer,
    InviteUsersToEventSerializer,
    RequestToParticipationSerializer,
)
from events.services import (
    bulk_accept_or_decline_invites_to_events,
    bulk_accpet_or_decline_requests_to_participation,
    invite_users_to_event,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from utils import (
    paginate_by_offset,
    skip_objects_from_response_by_id,
)


class InviteUsersToEvent(GenericAPIView):
    """
    Invite user to event

    This endpoint allows the author of the event
    and the user who is a participant in the event
    to send invitations to participate in this event
    """

    serializer_class: Type[Serializer] = InviteUsersToEventSerializer

    @swagger_auto_schema(tags=["invites-to-event"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = invite_users_to_event(
            event_id=serializer.validated_data["event_id"],
            users_ids=serializer.validated_data["ids"],
            request_user=request.user,
        )
        return Response(data, status=HTTP_200_OK)


@method_decorator(
    swagger_auto_schema(
        manual_parameters=[skip_param_query, offset_query], tags=["invites-to-event"]
    ),
    name="get",
)
@paginate_by_offset
class InvitesToEventList(ListAPIView):
    """
    List of my invitations to events

    This endpoint allows the user to
    view all of his event invitations.
    """

    serializer_class: Type[Serializer] = InvitesToEventListSerializer
    queryset: QuerySet[InviteToEvent] = InviteToEvent.get_all().filter(
        status=InviteToEvent.Status.WAITING
    )

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[InviteToEvent]:
        return self.queryset.filter(recipient=self.request.user)


class BulkAcceptOrDeclineInvitesToEvent(GenericAPIView):
    """
    Accepting/declining invitations to participate in an event

    This endpoint gives the user the ability to
    accept or decline requests to participate in events.
    """

    serializer_class: Type[
        Serializer
    ] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[Event] = InviteToEvent.get_all()

    @swagger_auto_schema(tags=["invites-to-event"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, int] = bulk_accept_or_decline_invites_to_events(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_200_OK)


@method_decorator(
    swagger_auto_schema(
        manual_parameters=[skip_param_query, offset_query], tags=["invites-to-event"]
    ),
    name="get",
)
@paginate_by_offset
class RequestToParticipationsList(ListAPIView):
    """
    List of requests for participation in the event

    This endpoint allows all users to view
    applications for participation in a
    particular private event
    """

    serializer_class: Type[Serializer] = RequestToParticipationSerializer
    queryset: QuerySet[
        RequestToParticipation
    ] = RequestToParticipation.get_all().filter(
        status=RequestToParticipation.Status.WAITING
    )

    @not_in_black_list
    @skip_objects_from_response_by_id
    def list(self, request: Request, pk: int) -> Response:

        try:
            event: Event = Event.objects.get(id=pk)
            queryset = self.queryset.filter(event=event)
            serializer = self.serializer_class(queryset, many=True)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Event.DoesNotExist:
            raise _404(object=Event)


class BulkAcceptOrDeclineRequestToParticipation(GenericAPIView):
    """
    Accepting/declining requests to participate in an event

    This endpoint allows the author of a private
    event to accept or reject applications for
    participation in his event.
    """

    serializer_class: Type[
        Serializer
    ] = BulkAcceptOrDeclineRequestToParticipationSerializer
    queryset: QuerySet[RequestToParticipation] = RequestToParticipation.get_all()

    @swagger_auto_schema(tags=["invites-to-event"])
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict[str, list[int]] = bulk_accpet_or_decline_requests_to_participation(
            data=serializer.validated_data, request_user=request.user
        )
        return Response(data, status=HTTP_200_OK)
