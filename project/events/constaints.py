APPLICATION_FOR_PARTICIPATION_SUCCESS: dict[str, str] = {'success': 'Your application for participation has been sent to the author of the event'}

ALREADY_SENT_REQUEST_TO_PARTICIPATE: dict[str, str] = {'error': 'You have already sent a request to participate'}

INVITE_USER_NOTIFICATION: str = '{user_name}, @{inviter_name},invited you to the event №{event_id}'
SENT_INVATION_ERROR: dict[str, str] = {'error': 'You cannot invite yourself to the event'} 
NEW_USER_ON_THE_EVENT_NOTIFICATION: str = '{author_name},for your event under the №{event_id} joined {user_type} player'
NEW_REQUEST_TO_PARTICIPATION: str = '{author_name},you have received a new request to participate in the event under the number №{event_id}'
NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE: str = 'new_request_to_participation'
NEW_USER_ON_THE_EVENT_MESSAGE_TYPE: str = 'new_user_on_the_event'
RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION: str = '{user_name},your application for participation in event №{event_id} was {response_type}'
RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE: str = 'response_to_request_for_participation' 


RESPONSE_TO_THE_INVITE_TO_EVENT: str = '{user_name},your user @{recipient_name} {recipient_last_name} invitation to the event №{event_id} was {response_type}'
RESPONSE_TO_THE_INVITE_TO_EVENT_MESSAGE_TYPE: str = 'response_to_invite_user_to_event' 


EVENT_DELETED_SUCCESS: dict[str, str] = {'success':  'Event deleted'}
EVENT_UPDATE_SUCCESS: dict[str, str] = {'success': 'Event updated'}
JOIN_TO_EVENT_SUCCESS: dict[str, str] = {'success': 'Join to event'}
DISCONNECT_FROM_EVENT_SUCCESS: dict[str, str] = {'success': 'Dicsonnect from event'}
SENT_INVATION_SUCCESS: dict[str, str] = {'success': 'Invation was sent'}
EVENT_NOT_FOUND_ERROR: dict[str, str] = {'error': 'Event not found'}
EVENT_AUTHOR_CAN_NOT_JOIN_ERROR: dict[str, str] = {'error': 'Author can`t join to his event'}
EVENT_TIME_EXPIRED_ERROR: dict[str, str] = {'error': 'Event time expired'}
BAD_EVENT_TIME_CREATE_ERROR: dict[str, str] = {'error': 'The time of the event must differ from the minimum by an hour'}
ALREADY_IN_EVENT_MEMBERS_LIST_ERROR: dict[str, str] = {'error': 'Already in the event members list'}
ALREADY_IN_EVENT_FANS_LIST_ERROR: dict[str, str] = {'error': 'Already in the event fans list'}
NO_IN_EVENT_MEMBERS_LIST_ERROR: dict[str, str] = {'error': 'You are not in event members list'}
NO_IN_EVENT_FANS_LIST_ERROR: dict[str, str] = {'error': 'You are not in event fans list'}
PASSWORD_CHANGE_ERROR: dict[str, str] = {'error': 'Password not change'}
NO_EVENT_PLACE_ERROR: dict[str, str] = {'error': 'No place'}
EVENT_TIME_NOTIFICATION_TEXT: dict[str, str] = 'Before the start of the event under the number {event_id} remained {time}. Dont forget to participate!'
ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR: dict[str, str] = {'error': 
    'You cannot join the event as a player because you are already a member of the event as a spectator'}
LEAVE_USER_FROM_THE_EVENT_NOTIFICATION: dict[str, str] = '{author_name},from your event under {event_id} player disconnected'
LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_MESSAGE_TYPE = 'leave_user_from_the_event'
NO_PRICE_DESK_ERROR: dict[str, str] = {'error': 'If the price is greater than 0 you must provide a description of what it is for'}

EVENT_TIME_NOTIFICATION_MESSAGE_TYPE: str ='event_time_notification'
INVITE_USER_TO_EVENT_MESSAGE_TYPE: str = 'invite_user_to_event'
EVENT_DELETE_MESSAGE_TYPE: str = 'event_deleted'
EVENT_UPDATE_MESSAGE_TYPE: str = 'event_updated'
EVENT_UPDATE_TEXT: str = 'the event №{event_id}, to which you subscribed as a participant, has been updated'
EVENT_DELETE_TEXT: str = 'the event №{event_id}, to which you subscribed as a participant, has been deleted'
AUTHOR_CAN_NOT_INVITE_ERROR: dict[str, str] = {'error': 'The author cannot be invited to his event'}

GET_PLANNED_EVENTS_ERROR: dict[str, str] = {'error': 'The user has hidden the list of his scheduled events'}


EVENT_TEMPLATE_UPDATE_SUCCESS: dict[str, str] = {'success': 'Event template updated'}
EVENT_TEMPLATE_NOT_FOUND_ERROR: dict[str, str] = {'error': 'Event template not found'}

SEND_INVATION_ERROR: dict[str, str] = {'error': 'You cannot invite users to this event'}

