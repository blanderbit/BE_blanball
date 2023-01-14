from typing import Union

from api_keys.models import ApiKey
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    Serializer,
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


class ValidateApiKeySerializer(Serializer):
    value = CharField(max_length=255)

    class Meta:
        fields: Union[str, list[str]] = ["value"]
