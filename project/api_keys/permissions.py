from api_keys.models import ApiKey
from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request


class ApiKeyPermission(BasePermission):
    """
    Access to endpoints only with a special admin api key
    """

    def has_permission(self, request: Request, view) -> bool:
        api_key_value: str = request.META.get("HTTP_APIKEY")
        try:
            api_key: ApiKey = ApiKey.objects.get(value=api_key_value)
            return ApiKey.check_api_key_status(api_key)
        except ApiKey.DoesNotExist:
            return False
