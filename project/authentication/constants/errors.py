# the error that means that the user's email has already been
# verified and he cannot send a verification request again
ALREADY_VERIFIED_ERROR: dict[str, str] = {"error": "account_already_verified"}

# error that means that the profile configuration field is required
CONFIGURATION_IS_REQUIRED_ERROR: dict[str, str] = {"error": "invalid_configuration"}

GET_PLANNED_EVENTS_ERROR: dict[str, str] = {"error": "invalid_get_planned_events"}

# the error that means that when registering or updating
# a profile, an age of more than 80 years was indicated
MAX_AGE_VALUE_ERROR: dict[str, str] = {"error": "age_over_80_years"}

# the error that means that when registering or updating
# a profile, an age of less than 6 years was indicated
MIN_AGE_VALUE_ERROR: dict[str, str] = {"error": "age_less_6_years"}

# the error that means that the user's password
# does not match his current password
WRONG_PASSWORD_ERROR: dict[str, str] = {"error": "wrong_old_password"}

# the error meaning that the passwords entered by the user do not match
PASSWORDS_DO_NOT_MATCH_ERROR: dict[str, str] = {"error": "passwords_do_not_match"}

# the error that means that the user entered
# incorrect data to enter the account
INVALID_CREDENTIALS_ERROR: dict[str, str] = {"error": "invalid_credentials"}

# the error that means that the user's email
# has not yet been verified and he does not
# have access to some part of the functionality
NOT_VERIFIED_BY_EMAIL_ERROR: dict[str, str] = {"error": "not_verified"}

# the error that means that the user does not
# have access to the action for some reason
NO_PERMISSIONS_ERROR: dict[str, str] = {"error": "no_permissions"}

# the error that means that the refresh token is invalid
INVALID_REFRESH_TOKEN: dict[str, str] = {"error": "invalid_refresh_token"}

# the error that means that the user
# entered an invalid confirmation code
BAD_CODE_ERROR: dict[str, str] = {"error": "bad_verify_code"}

# the error that means that the verification code has expired
CODE_EXPIRED_ERROR: str = {"error": "verify_code_expired"}

# the error that means that the email entered by the user is already in use
THIS_EMAIL_ALREADY_IN_USE_ERROR: dict[str, str] = {"error": "email_already_in_use"}

# the error that means that the image uploaded by the
# user exceeds the weight limit
AVATAR_MAX_SIZE_ERROR: dict[str, str] = {"error": "avatar_max_size_1mb"}
