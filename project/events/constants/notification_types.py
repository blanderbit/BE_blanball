# the type of notification that will be sent
# to the user if the participant left his event
LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_TYPE: str = "leave_from_the_event"

# the type of notification that will be sent when the
# user receives a new request to participate in the event
NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TYPE: str = "new_request_to_participation"

# the type of notification that will be
# sent if the user is invited to the event
INVITE_USER_TO_EVENT_NOTIFICATION_TYPE: str = "invite_user_to_event"

# the type of notification that the user will
# receive if the event at which he was a participant
# or a spectator was canceled
EVENT_DELETE_NOTIFICATION_TYPE: str = "event_deleted"

# the type of notification that the user will

# receive if the event at which he was a participant
# or a spectator was updated
EVENT_UPDATE_NOTIFICATION_TYPE: str = "event_updated"

# the type of notification that will be sent
# to all users of the event as a reminder
# of the start of this event
EVENT_TIME_NOTIFICATION_TYPE: str = "event_time_notification"

# the type of notification that will be sent
# to the user if his event invitation was accepted or rejected
RESPONSE_TO_THE_INVITE_TO_EVENT_NOTIFICATION_TYPE: str = (
    "response_to_invite_user_to_event"
)

# the type of notification that will be sent to the user
# if his request to participate in the event was accepted or rejected
RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_NOTIFICATION_TYPE: str = (
    "response_to_request_for_participation"
)

# the type of notification that will be sent
# to the user if a new user is added to his event
NEW_USER_ON_THE_EVENT_NOTIFICATION_TYPE: str = "new_user_on_the_event"

# the type of notification that will be sent
# to the user if the final user is added to his event
LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE: str = "last_user_on_the_event"

YOU_ARE_LAST_USER_ON_THE_EVENT_NOTIFICATION_TYPE: str = "you_are_last_user_on_the_event"

# the type of notification that will be
# sent to the user if he was kicked out of the event
USER_REMOVE_FROM_EVENT_NOTIFICATION_TYPE: str = "remove_from_event"

# the type of notification that the user will
# receive if the event in which he participates has ended
EVENT_HAS_BEEN_ENDEN_NOTIFICATION_TYPE: str = "event_has_been_ended"

# ======================= SERVICE MESSAGES =================================
# such messages are not shown to the user and are not stored in the database.
# They are only needed to update data on the client side of the application in real time.

# SERVICE MESSAGE that is sent to the user when he
# accepts or rejects requests to participate in his event.
UPDATE_MESSAGE_ACCEPT_OR_DECLINE_INVITE_TO_EVENT: str = (
    "update_message_accept_or_decline_invite_to_event"
)

# SERVICE MESSAGE that will be sent to the user when he accepts
# or rejects a request to participate in the event from another user
UPDATE_MESSAGE_ACCEPT_OR_DECLINE_REQUEST_TO_PARTICIPATION: str = (
    "update_message_accept_or_decline_request_to_participation"
)
# ==============================================================================
