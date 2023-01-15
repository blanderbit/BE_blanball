# the error indicating that the user cannot 
# resubmit the request to participate in the event
ALREADY_SENT_REQUEST_TO_PARTICIPATE_ERROR: dict[str, str] = {
    "error": "already_sent_request_to_participate"
}

# the error that means that the user 
# cannot join his event as a participant
EVENT_AUTHOR_CAN_NOT_JOIN_ERROR: dict[str, str] = {
    "error": "author_cant_enter_his_event"
}

# the error meaning that the time to enter 
# the event as a participant or spectator has ended
EVENT_TIME_EXPIRED_ERROR: dict[str, str] = {"error": "event_time_expired"}

# the error that means that when creating 
# an event, the user specified an incorrect start date
BAD_EVENT_TIME_CREATE_ERROR: dict[str, str] = {"error": "bad_event_date_time"}

# the error that means that the user is already 
# in the list of event participants
ALREADY_IN_EVENT_MEMBERS_LIST_ERROR: dict[str, str] = {"error": "already_like_member"}

# the error that means that the user is already 
# in the list of event fans
ALREADY_IN_EVENT_FANS_LIST_ERROR: dict[str, str] = {"error": "already_like_fan"}

# the error that means that the user is not in the list of event participants
NO_IN_EVENT_MEMBERS_LIST_ERROR: dict[str, str] = {"error": "not_in_event_members_list"}

# the error that means that the user is not in the list of event fans
NO_IN_EVENT_FANS_LIST_ERROR: dict[str, str] = {"error": "not_in_event_fans_list"}

# the error that means that there are no 
# free places for participation at the event
NO_EVENT_PLACE_ERROR: dict[str, str] = {"error": "no_place"}


# the an error that means that the author 
# cannot be invited to his own event
AUTHOR_CAN_NOT_INVITE_ERROR: dict[str, str] = {
    "error": "author_cannot_be_invited_to_his_event"
}
GET_PLANNED_EVENTS_ERROR: dict[str, str] = {"error": "hidden_planned_events"}

# the error that means that the user does 
# not have rights to invite anyone to this event
USER_CAN_NOT_INVITE_TO_THIS_EVENT_ERROR: dict[str, str] = {
    "error": "no_permissions_to_invite"
}

# the error that means that the user to whom 
# the event invitation was sent cannot be invited
THIS_USER_CAN_NOT_BE_INVITED: dict[str, str] = {"error": "this_user_cannot_be_invited"}

# the error that means that when creating an event, 
# the price was specified but the price description was not specified
NO_PRICE_DESK_ERROR: dict[str, str] = {"error": "price_description_required"}

# the  error that means that the user cannot invite himself to the event
CAN_NOT_INVITE_YOURSELF: dict[str, str] = {"error": "cant_invite_yourself"}
