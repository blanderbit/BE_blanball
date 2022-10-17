ADMIN_ROLE: str = 'Admin'
USER_ROLE: str = 'User'

MAX_AGE_VALUE_ERROR: dict[str, str] = {'error': 'Age must not exceed 100 years old'}
MIN_AGE_VALUE_ERROR: dict[str, str] = {'error': 'Age must be at least 6 years old'}

ALREADY_VERIFIED_ERROR: dict[str, str] = {'error':'Your account is already verified'}

CHANGE_PASSWORD_SUCCESS: dict[str, str] = {'succes' : 'Password change'}
REGISTER_SUCCESS_TITLE: str = 'Thank you for registering with BlanBall'
REGISTER_SUCCESS_TEXT: str = 'You received this message because this email is registered in the BlanBall app.'

PASS_UPDATE_SUCCESS_BODY_TITLE: str  = 'Password change was successful'
PASS_UPDATE_SUCCESS_TITLE: str = 'Your password has been changed'
PASS_UPDATE_SUCCESS_TEXT: str = 'You received this message because your password has been changed in BlanBall.'

CHANGE_PHONE_SUCCESS: dict[str, str] = {'succes' : 'Phone change'}
CHANGE_EMAIL_SUCCESS: dict[str, str] = {'succes' : 'Email change'}
CONFIGURATION_IS_REQUIRED_ERROR: dict[str, str] = {'error': 'Сonfiguration should contain fields like: email,phone,send_email,show_my_planned_events'}

WRONG_PASSWORD_ERROR: dict[str, str] = {'error': 'Wrong old password'}
PASSWORDS_DO_NOT_MATCH: dict[str, str] = {'error': 'Passwords do not match'}
NO_EMAIL_REGISTRATION_ERROR: dict[str, str] = {'error': 'Users should have a Email'}
INVALID_CREDENTIALS_ERROR: dict[str, str] =  {'error': 'Invalid credentials, try again'}
NOT_VERIFIED_BY_EMAIL_ERROR: dict[str, str] = {'error': 'Email is not verified'}
NO_SUCH_USER_ERROR: dict[str, str] = {'error': 'No such user'}
NO_PERMISSIONS_ERROR: dict[str, str] = {'error': 'You have no permissions to do this'}

THIS_EMAIL_ALREADY_IN_USE_ERROR: dict[str, str] = {'error': 'This email is already in use'}
ACTIVATION_SUCCESS: dict[str, str] = {'success': 'Activation by email'}
ACCOUNT_DELETED_SUCCESS: dict[str, str] = {'success':  'Account deleted'}
PASSWORD_RESET_SUCCESS: dict[str, str] = {'success': 'Password reset'}


BAD_CODE_ERROR: dict[str, str] = {'error': 'Bad verify code'}
CODE_EXPIRED_ERROR: dict[str, str] = {'error': 'This code expired'} 
PASSWORD_RESET_CODE_TYPE: str  = 'password_reset'
EMAIL_VERIFY_CODE_TYPE: str = 'email_verify'
PASSWORD_CHANGE_CODE_TYPE: str = 'password_change'
EMAIL_CHANGE_CODE_TYPE: str = 'email_change'
PHONE_CHANGE_CODE_TYPE: str = 'phone_change'
ACCOUNT_DELETE_CODE_TYPE: str = 'accoount_delete'
SENT_CODE_TO_EMAIL_SUCCESS: str = {'success': 'We have sent you a code to email'}

EMAIL_MESSAGE_TEMPLATE_TITLE: str = '{type} {key} in the Blanball app'


REGISTER_SUCCESS_BODY_TITLE: str = 'Registration was successful'
REGISTER_SUCCESS_TITLE: str = 'Thank you for registering with BlanBall'
REGISTER_SUCCESS_TEXT: str = 'You received this message because this email is registered in the BlanBall app.'


ACCOUNT_DELETE_SUCCESS_BODY_TITLE: str = 'Account successfully deleted'
ACCOUNT_DELETE_SUCCESS_TITLE: str = 'Thank you for using our app'
ACCOUNT_DELETE_SUCCESS_TEXT: str = 'You received this message because your account has been deleted in the BlanBall app.'

TEMPLATE_SUCCESS_BODY_TITLE: str  = 'Change {key} passed successfully'
TEMPLATE_SUCCESS_TITLE: str = 'Your {key} changed!'
TEMPLATE_SUCCESS_TEXT: str = 'You received this message because your {key} has been changed in the BlanBall application.'

EMAIL_VERIFY_SUCCESS_BODY_TITLE: str = 'Verification was successful!'
EMAIL_VERIFY_SUCCESS_TEXT: str = 'You received this message because your account has been verified in the BlanBall application.'
EMAIL_VERIFY_SUCCESS_TITLE: str = 'Your account has been verified!'
GET_PLANNED_IVENTS_ERROR: dict[str, str] = {'error': 'Get planned ivents can only contain: day(d), month(m) and year(y)'}
BLANBALL: str = 'BlanBall'

NO_SUCH_IMAGE_ERROR: dict[str, str] = {'error': 'Image not found'}