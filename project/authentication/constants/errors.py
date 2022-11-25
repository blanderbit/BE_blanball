ALREADY_VERIFIED_ERROR: dict[str, str] = {"error": "account_already_verified"}

CONFIGURATION_IS_REQUIRED_ERROR: dict[str, str] = {"error": "invalid_configuration"}

GET_PLANNED_EVENTS_ERROR: dict[str, str] = {"error": "invalid_get_planned_events"}

MAX_AGE_VALUE_ERROR: dict[str, str] = {"error": "age_over_80_years"}
MIN_AGE_VALUE_ERROR: dict[str, str] = {"error": "age_less_6_years"}

WRONG_PASSWORD_ERROR: dict[str, str] = {"error": "wrong_old_password"}
PASSWORDS_DO_NOT_MATCH_ERROR: dict[str, str] = {"error": "passwords_do_not_match"}
INVALID_CREDENTIALS_ERROR: dict[str, str] = {"error": "invalid_credentials"}
NOT_VERIFIED_BY_EMAIL_ERROR: dict[str, str] = {"error": "not_verified"}
NO_PERMISSIONS_ERROR: dict[str, str] = {"error": "no_permissions"}
BAD_CODE_ERROR: dict[str, str] = {"error": "bad_verify_code"}

CODE_EXPIRED_ERROR: str = {"error": "verify_code_expired"}

THIS_EMAIL_ALREADY_IN_USE_ERROR: dict[str, str] = {"error": "email_already_in_use"}
