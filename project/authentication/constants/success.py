# the response message that indicates that
# the user's account was successfully verified
ACTIVATION_SUCCESS: dict[str, str] = {"success": "verified_account"}

# the response message that indicates that
# the user's account was successfully deleted
ACCOUNT_DELETED_SUCCESS: dict[str, str] = {"success": "account_deleted"}

# the response message that indicates
# that the user's password was successfully reset
PASSWORD_RESET_SUCCESS: dict[str, str] = {"success": "password_reset"}

# the response message that indicates that the reset password verify code
# entered by the user is absolutely valid
RESET_PASSWORD_CODE_IS_VALID_SUCCESS: dict[str, str] = {"success": "code_is_valid"}

# the response message that indicates that the phone
# number entered by the user is absolutely valid
PHONE_IS_VALID_SUCCESS: dict[str, str] = {"success": "phone_is_valid"}

# the response message that indicates
# that the user's avatar was successfully changed
PROFILE_AVATAR_UPDATED_SUCCESS: dict[str, str] = {"success": "profile_avatar_updated"}

# the response message that indicates that the
# confirmation code was successfully sent to the email
SENT_CODE_TO_EMAIL_SUCCESS: dict[str, str] = {"success": "sent_code_to_email"}

# the response message that indicates
# that the user's email was successfully changed
CHANGE_EMAIL_SUCCESS: dict[str, str] = {"succes": "email_change"}

# the response message that indicates
# that the user's password was successfully changed
CHANGE_PASSWORD_SUCCESS: dict[str, str] = {"succes": "password_change"}


REGISTER_SUCCESS_TITLE: str = "Thank you for registering with BlanBall"
REGISTER_SUCCESS_TEXT: str = (
    "You received this message because this email is registered in the BlanBall app."
)

PASS_UPDATE_SUCCESS_BODY_TITLE: str = "Password change was successful"
PASS_UPDATE_SUCCESS_TITLE: str = "Your password has been changed"
PASS_UPDATE_SUCCESS_TEXT: str = (
    "You received this message because your password has been changed in BlanBall."
)

EMAIL_MESSAGE_TEMPLATE_TITLE: str = "{type} {key} in the Blanball app"


REGISTER_SUCCESS_BODY_TITLE: str = "Registration was successful"
REGISTER_SUCCESS_TITLE: str = "Thank you for registering with BlanBall"
REGISTER_SUCCESS_TEXT: str = (
    "You received this message because this email is registered in the BlanBall app."
)


ACCOUNT_DELETE_SUCCESS_BODY_TITLE: str = "Account successfully deleted"
ACCOUNT_DELETE_SUCCESS_TITLE: str = "Thank you for using our app"
ACCOUNT_DELETE_SUCCESS_TEXT: str = "You received this message because your account has been deleted in the BlanBall app."

TEMPLATE_SUCCESS_BODY_TITLE: str = "Change {key} passed successfully"
TEMPLATE_SUCCESS_TITLE: str = "Your {key} changed!"
TEMPLATE_SUCCESS_TEXT: str = "You received this message because your {key} has been changed in the BlanBall application."

EMAIL_VERIFY_SUCCESS_BODY_TITLE: str = "Verification was successful!"
EMAIL_VERIFY_SUCCESS_TEXT: str = "You received this message because your account has been verified in the BlanBall application."
EMAIL_VERIFY_SUCCESS_TITLE: str = "Your account has been verified!"
BLANBALL: str = "BlanBall"
