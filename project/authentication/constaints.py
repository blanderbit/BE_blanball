ADMIN_ROLE = 'Admin'
USER_ROLE = 'User'

MAX_AGE_VALUE_ERROR = {'error': 'Age must not exceed 100 years old'}
MIN_AGE_VALUE_ERROR = {'error': 'Age must be at least 6 years old'}

ALREADY_VERIFIED_ERROR = {'error':'Your account is already verified'}

CHANGE_PASSWORD_SUCCESS = {'succes' : 'Password change'}
REGISTER_SUCCESS_TITLE = 'Thank you for registering with BlanBall'
REGISTER_SUCCESS_TEXT = 'You received this message because this email is registered in the BlanBall app.'

PASS_UPDATE_SUCCESS_BODY_TITLE  = 'Password change was successful'
PASS_UPDATE_SUCCESS_TITLE = 'Your password has been changed'
PASS_UPDATE_SUCCESS_TEXT = 'You received this message because your password has been changed in BlanBall.'

CHANGE_PHONE_SUCCESS = {'succes' : 'Phone change'}
CHANGE_EMAIL_SUCCESS = {'succes' : 'Email change'}
CONFIGURATION_IS_REQUIRED_ERROR = {'error': 'Сonfiguration should contain fields like: email,phone,send_email'}

WRONG_PASSWORD_ERROR = {'error': 'Wrong old password'}
PASSWORDS_DO_NOT_MATCH = {'error': 'Passwords do not match'}
NO_EMAIL_REGISTRATION_ERROR = {'error': 'Users should have a Email'}
INVALID_CREDENTIALS_ERROR =  {'error': 'Invalid credentials, try again'}
NOT_VERIFIED_BY_EMAIL_ERROR = {'error': 'Email is not verified'}
NO_SUCH_USER_ERROR = {'error': 'No such user'}
NO_PERMISSIONS_ERROR = {'error': 'You have no permissions to do this'}

THIS_EMAIL_ALREADY_IN_USE_ERROR = {'error': 'This email is already in use'}
ACTIVATION_SUCCESS = {'success': 'Activation by email'}
ACCOUNT_DELETED_SUCCESS = {'success':  'Account deleted'}
PASSWORD_RESET_SUCCESS = {'success': 'Password reset'}


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

EMAIL_MESSAGE_TEMPLATE_TITLE = '{type} {key} in the Blanball app'


REGISTER_SUCCESS_BODY_TITLE = 'Registration was successful'
REGISTER_SUCCESS_TITLE = 'Thank you for registering with BlanBall'
REGISTER_SUCCESS_TEXT = 'You received this message because this email is registered in the BlanBall app.'

TEMPLATE_SUCCESS_BODY_TITLE  = 'Change {key} passed successfully'
TEMPLATE_SUCCESS_TITLE = 'Your {key} changed!'
TEMPLATE_SUCCESS_TEXT = 'You received this message because your {key} has been changed in the BlanBall application.'

EMAIL_VERIFY_SUCCESS_BODY_TITLE = 'Verification was successful!'
EMAIL_VERIFY_SUCCESS_TITLE = 'Your account has been activated!'
GET_PLANNED_IVENTS_ERROR = {'error': 'Get planned ivents can only contain: day(d), month(m) and year(y)'}
BLANBALL = 'BlanBall'