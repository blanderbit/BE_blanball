#ROLES
ADMIN_ROLE = "Admin"
USER_ROLE = "User"

#CHANGE & CREATE & RESET
THIS_EMAIL_ALREADY_IN_USE_ERROR = {'error': 'This email is already in use'}
CHANGE_PHONE_SUCCESS = {'succes' : 'Phone change'}
CHANGE_EMAIL_SUCCESS = {'succes' : 'Email change'}
CHANGE_PASSWORD_SUCCESS = {'succes' : 'Password change'}
REVIEW_CREATE_SUCCESS = {'success': 'Review create'}
ACTIVATION_SUCCESS = {'success': 'Activation by email'}
ACCOUNT_DELETED_SUCCESS = {'success':  'Account deleted'}
PASSWORD_RESET_SUCCESS = {'success': 'Password reset'}
CREATE_EVENT_ERROR = {'error': 'You cannot invite more people than the number of '}

#EVENT
EVENT_DELETED_SUCCESS = {'success':  'Event deleted'}
EVENT_UPDATE_SUCCESS = {'success': 'Event updated'}
JOIN_TO_EVENT_SUCCESS = {'success': 'Join to event'}
DISCONNECT_FROM_EVENT_SUCCESS = {'success': 'Dicsonnect from event'}
EVENT_NOT_FOUND_ERROR = {'error': 'Event not found'}
EVENT_AUTHOR_CAN_NOT_JOIN_ERROR = {'error': 'Author can`t join to your event'}
EVENT_TIME_EXPIRED_ERROR = {'error': 'Event time expired'}
BAD_EVENT_TIME_CREATE_ERROR = {'error': 'The time of the event must differ from the minimum by an hour'}
ALREADY_IN_EVENT_MEMBERS_LIST_ERROR = {'error': 'Already in the event members list'}
ALREADY_IN_EVENT_FANS_LIST_ERROR = {'error': 'You are already in the event fans list'}
NO_IN_EVENT_MEMBERS_LIST_ERROR = {'error': 'You are not in event members list'}
NO_IN_EVENT_FANS_LIST_ERROR = {'error': 'You are not in event fans list'}
PASSWORD_CHANGE_ERROR = {'error': 'Password not change'}
GET_PLANNED_IVENTS_ERROR = {'error': 'Get planned ivents can only contain: day(d), month(m) and year(y)'}
NO_EVENT_PLACE_ERROR = {'error': 'No place'}
ALREADY_IN_EVENT_LIKE_SPECTATOR_ERROR = {'error':'You cannot join the event as a player because you are already a member of the event as a spectator'}


#CODE
BAD_CODE_ERROR = {'error': 'Bad verify code'}
CODE_EXPIRED_ERROR = {'error': 'This code expired'} 
PASSWORD_RESET_CODE_TYPE  = 'password_reset'
EMAIL_VERIFY_CODE_TYPE = 'email_verify'
PASSWORD_CHANGE_CODE_TYPE = 'password_change'
EMAIL_CHANGE_CODE_TYPE = 'email_change'
PHONE_CHANGE_CODE_TYPE = 'phone_change'
ACCOUNT_DELETE_CODE_TYPE = 'accoount_delete'
CODE_EXPIRE_MINUTES_TIME = 5
SENT_CODE_TO_EMAIL_SUCCESS = {'success': 'We have sent you a code to email'}

#MAINTENANCE
MAINTENANCE_UPDATED_SUCCESS = {'success': 'Maintenance updated success'}
MAINTENANCE_CAN_NOT_UPDATE_ERROR = {'error': 'Can not update maintenance'}
MAINTENANCE_TRUE_NOTIFICATION_TEXT = '{username} {last_name}, tech roboty True'
MAINTENANCE_FALSE_NOTIFICATION_TEXT = '{username} {last_name}, tech roboty False'

#VALIDATION 
WRONG_PASSWORD_ERROR = {'error': 'Wrong old password'}
PASSWORDS_DO_NOT_MATCH = {'error': 'Passwords do not match'}
NO_EMAIL_REGISTRATION_ERROR = {'error': 'Users should have a Email'}
INVALID_CREDENTIALS_ERROR =  {'error': 'Invalid credentials, try again'}
NOT_VERIFIED_BY_EMAIL_ERROR = {'error': 'Email is not verified'}
NO_SUCH_USER_ERROR = {'error': 'No such user'}
NO_PERMISSIONS_ERROR = {'error': 'You have no permissions to do this'}
REVIEW_CREATE_ERROR = {'error':'You cant leave a review for yourself'}
CANNOT_HIDE_SHOW_THIS_FIELD_ERROR = 'error : You cannot hide or show fields:{key}'
MAX_AGE_VALUE_ERROR = {'error': 'Age must not exceed 100 years old'}
MIN_AGE_VALUE_ERROR = {'error': 'Age must be at least 6 years old'}
CONFIGURATION_IS_REQUIRED_ERROR = {'error': 'Сonfiguration should contain fields like: email,phone,send_email'}


EMAIL_MESSAGE_TEMPLATE_TITLE = '{type} {key} у додатку Blanball'

INVITE_USER_NOTIFICATION = '@{user_name},запросив вас на подію {event_name}'

SENT_INVATION_SUCCESS = {'success':'Invation was sent'}

SENT_INVATION_ERROR = {'error': 'You cannot invite yourself to the event'} 

NO_PRICE_DESK_ERROR = {'error':'If the price is greater than 0 you must provide a description of what it is for'}

AFTER_REGISTER_SEND_EMAIL_TEXT = '{user_name} {user_last_name},дякуємо вам за регестрацію в нашому додатку Blanball!'

AFTER_ACCOUNT_DELETED_EMAIL_TEXT = '{user_name} {user_last_name},ваш аккаунт було успішно видалено з додатку Blanball!'

AFTER_RESET_PASSWORD_EMAIL_TEXT = '{user_name} {user_last_name},ваш пароль було успішно змінено!'

NEW_USER_ON_THE_EVENT_NOTIFICATION = '{author_name},на вашу подію під номером {event_id} долучився {user_type} гравець'

NEW_REQUEST_TO_PARTICIPATION = '{author_name},вам надійшов новий запит на участь у події під номером №{event_id}'
NEW_REQUEST_TO_PARTICIPATION_MESSAGE_TYPE = 'new_request_to_participation'

NEW_USER_ON_THE_EVENT_MESSAGE_TYPE = 'new_user_on_the_event'

ALREADY_VERIFIED_ERROR = {'error':'Your account is already verified'}

APPLICATION_FOR_PARTICIPATION_SUCCESS = {'success':'Your application for participation has been sent to the author of the event'}

ALREADY_SENT_REQUEST_TO_PARTICIPATE = {'error':'You have already sent a request to participate'}

CONFIG_FILE_ERROR = {'error':'Config file is not available now'}

INVITE_USER_TO_EVENT_MESSAGE_TYPE = 'invite_user_to_event'
EVENT_DELETE_MESSAGE_TYPE = 'event_deleted'
EVENT_UPDATE_MESSAGE_TYPE = 'event_updated'
CHANGE_MAINTENANCE_MESSAGE_TYPE = 'change_maintenance'
EVENT_TIME_NOTIFICATION_MESSAGE_TYPE ='event_time_notification'
REVIEW_CREATE_MESSAGE_TYPE = 'review_creaete'