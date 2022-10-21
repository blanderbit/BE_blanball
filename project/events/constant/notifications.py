EVENT_UPDATE_NOTIFICATION_TEXT: str = 'the event №{event_id}, to which you subscribed as a participant, has been updated'
EVENT_DELETE_NOTIFICATION_TEXT: str = 'the event №{event_id}, to which you subscribed as a participant, has been deleted'
LEAVE_USER_FROM_THE_EVENT_NOTIFICATION_TEXT: str = '{author_name},from your event under {event_id} player disconnected'
INVITE_USER_NOTIFICATION_TEXT: str = '{user_name}, @{inviter_name},invited you to the event №{event_id}'
NEW_USER_ON_THE_EVENT_NOTIFICATION_TEXT: str = '{author_name},for your event under the №{event_id} joined {user_type} player'
NEW_REQUEST_TO_PARTICIPATION_NOTIFICATION_TEXT: str = '{author_name},you have received a new request to participate in the event under the number №{event_id}'
RESPONSE_TO_THE_INVITE_TO_EVENT_NOTIFICATION_TEXT: str = '{user_name},your user @{recipient_name} {recipient_last_name} invitation to the event №{event_id} was {response_type}'

LEAVE_USER_FROM_THE_EVENT_MESSAGE_TYPE: str = 'leave_from_the_event'
NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE: str = 'new_request_to_participation'
INVITE_USER_TO_EVENT_MESSAGE_TYPE: str = 'invite_user_to_event'
EVENT_DELETE_MESSAGE_TYPE: str = 'event_deleted'
EVENT_UPDATE_MESSAGE_TYPE: str = 'event_updated'
EVENT_TIME_NOTIFICATION_MESSAGE_TYPE: str ='event_time_notification'
RESPONSE_TO_THE_INVITE_TO_EVENT_MESSAGE_TYPE: str = 'response_to_invite_user_to_event' 
RESPONSE_TO_THE_REQUEST_FOR_PARTICIPATION_MESSAGE_TYPE: str = 'response_to_request_for_participation' 
NEW_USER_ON_THE_EVENT_MESSAGE_TYPE: str = 'new_user_on_the_event'
USER_REMOVE_FROM_EVENT_MESSAGE_TYPE: str = 'remove_from_event'


data = {
                'recipient': {
                    'id': event.author.id,
                    'name': event.author.profile.name,
                    'last_name': event.author.profile.last_name
                },
                'event': {
                    'id': event.id
                },
                'sender': {
                    'id': user.id,
                    'name': user.profile.name,
                    'last_name': user.profile.last_name
                }
            })