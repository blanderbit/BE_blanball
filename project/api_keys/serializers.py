from rest_framework import serializers
from api_keys.models import ApiKey
from typing import Union


class CreateApiKeySerializer(serializers.ModelSerializer):

    class Meta:
        model: ApiKey = ApiKey
        fields: Union[str, list[str]] = [
            "expire_time",
        ]

class ApiKeysListSerializer(serializers.ModelSerializer):

    class Meta:
        model: ApiKey = ApiKey
        fields: Union[str, list[str]] = '__all__'