from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from typing import Type
from django.db.models.query import QuerySet
from api_keys.serializers import (
    CreateApiKeySerializer,
    ApiKeysListSerializer,
)
from api_keys.models import (
    ApiKey
)

class CreateApiKey(GenericAPIView):
    """
    Create api key

    This endpoint allows "admin" users to 
    create new api keys to access admin endpoints
    """

    serializer_class: Type[Serializer] = CreateApiKeySerializer
    queryset: QuerySet[ApiKey] = ApiKey.objects.all()


    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_key: ApiKey = ApiKey.objects.create(**serializer.validated_data)
        return Response(
            {
                "value": api_key.value,
                "exprire_time": api_key.expire_time,
            }, 
            HTTP_201_CREATED)


class ApiKeysList(ListAPIView):
    """
    Api keys list

    This endpoint allows "admin" users to 
    get a list of all the api keys
    """
    serializer_class: Type[Serializer] = ApiKeysListSerializer
    queryset: QuerySet[ApiKey] = ApiKey.get_only_active()