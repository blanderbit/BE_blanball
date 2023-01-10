from typing import Union

from api_keys.models import ApiKey
from rest_framework.serializers import (
    ModelSerializer
)


class CreateApiKeySerializer(ModelSerializer):
    class Meta:
        model: ApiKey = ApiKey
        fields: Union[str, list[str]] = [
            "expire_time",
        ]


class ApiKeysListSerializer(ModelSerializer):
    class Meta:
        model: ApiKey = ApiKey
        fields: Union[str, list[str]] = "__all__"
