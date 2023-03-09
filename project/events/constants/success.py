# the response message which means that
# the event was successfully deleted
EVENT_DELETED_SUCCESS: dict[str, str] = {"success": "event_deleted"}

# the response message which means that
# the event was successfully deleted
EVENT_UPDATE_SUCCESS: dict[str, str] = {"success": "event_updated"}

# the response message which means that the request
# to participate in the event was successfully sent
SENT_REQUEST_TO_PARTICIPATION_SUCCESS: dict[str, str] = {
    "success": "sent_request_to_participation"
}

# the response message that means that the user
# has successfully joined the event as a participant
JOIN_TO_EVENT_SUCCESS: dict[str, str] = {"success": "join_to_event"}

# the response message that means that the user
# has successfully disconnected  from the event
DISCONNECT_FROM_EVENT_SUCCESS: dict[str, str] = {"success": "dicsonnect_from_event"}

# the response message that means the user was successfully kicked out of the event
USER_REMOVED_FROM_EVENT_SUCCESS: dict[str, str] = {"success": "removed_user_from_event"}

# the response message that means that
# the event invitation was sent successfully
SENT_INVATION_SUCCESS: dict[str, str] = {"success": "sent_invite"}
