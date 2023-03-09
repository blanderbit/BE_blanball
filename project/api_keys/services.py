from api_keys.constants.errors import (
    API_KEY_EXPIRED_ERROR,
)
from api_keys.models import ApiKey
from config.exceptions import _404
from rest_framework.serializers import (
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


def bulk_delete_api_keys(*, ids: dict[str, int]) -> None:
    for api_key_id in ids:
        try:
            ApiKey.objects.get(id=api_key_id).delete()
            yield api_key_id
        except ApiKey.DoesNotExist:
            pass


def validate_api_key(*, api_key: str) -> None:
    try:
        api_key: ApiKey = ApiKey.objects.get(value=api_key)
        if api_key.check_api_key_status():
            pass
        else:
            raise ValidationError(API_KEY_EXPIRED_ERROR, HTTP_400_BAD_REQUEST)
    except ApiKey.DoesNotExist:
        raise _404(object=ApiKey)
