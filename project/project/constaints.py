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

#EVENT
EVENT_DELETED_SUCCESS = {'success':  'Event deleted'}
EVENT_UPDATE_SUCCESS = {'success': 'Event updated'}
JOIN_EVENT_SUCCES = {'success': 'Join to event'}
DISCONNECT_FROM_EVENT_SUCCESS = {'success': 'Dicsonnect from event'}
EVENT_NOT_FOUND_ERROR = {'error': 'Event not found'}
EVENT_AUTHOR_CAN_NOT_JOIN_ERROR = {'error': 'Author can`t join to your event'}
EVENT_TIME_EXPIRED_ERROR = {'error': 'Event time expired'}
BAD_EVENT_TIME_CREATE_ERROR = {'error': 'The time of the event must differ from the minimum by an hour'}
ALREADY_IN_EVENT_MEMBERS_LIST_ERROR = {'error': 'You are already in the event members list'}
ALREADY_IN_EVENT_FANS_LIST_ERROR = {'error': 'You are already in the event fans list'}
NO_IN_EVENT_MEMBERS_LIST_ERROR = {'error': 'You are not in event members list'}
NO_IN_EVENT_FANS_LIST_ERROR = {'error': 'You are not in event fans list'}
PASSWORD_CHANGE_ERROR = {'error': 'Password not change'}
GET_PLANNED_IVENTS_ERROR = {'error': 'Get planned ivents can only contain: day(d), month(m) and year(y)'}
NO_EVENT_PLACE_ERROR = {'error': 'No place'}


#CODE
BAD_CODE_ERROR = {'error': 'Bad verify code'}
CODE_EXPIRED_ERROR = {'error': 'This code expired'} 
PASSWORD_RESET_CODE_TYPE  = 'password_reset'
EMAIL_VERIFY_CODE_TYPE = 'email_verify'
PASSWORD_CHANGE_CODE_TYPE = 'password_change'
EMAIL_CHANGE_CODE_TYPE = 'email_change'
PHONE_CHANGE_CODE_TYPE = 'phone_change'
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
CONFIGURATION_IS_REQUIRED_ERROR = {'error': 'Configuration is required field'}


EMAIL_MESSAGE_TEMPLATE_TITLE = '{type} {key} у додатку Blanball'

INVITE_USER_NOTIFICATION = '@{user_name},запросив вас на подію під номерм: №{event_id}'

SENT_INVATION_SUCCESS = {'success':'Invation was sent'}

SENT_INVATION_ERROR = {'error': 'You cannot invite yourself to the event'} 