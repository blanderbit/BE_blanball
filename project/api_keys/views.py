from typing import Type

from api_keys.constants.success import (
    API_KEY_IS_VALID_SUCCESS,
)
from api_keys.filters import (
    API_KEYS_LIST_ORDERING_FIELDS,
    API_KEYS_LIST_SEARCH_FIELDS,
)
from api_keys.models import ApiKey
from api_keys.openapi import (
    api_keys_list_query_params,
)
from api_keys.permissions import ApiKeyPermission
from api_keys.serializers import (
    ApiKeysListSerializer,
    CreateApiKeySerializer,
    ValidateApiKeySerializer,
)
from api_keys.services import (
    bulk_delete_api_keys,
    validate_api_key,
)
from authentication.permissions import AllowAny
from config.serializers import (
    BaseBulkSerializer,
)
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from events.services import (
    skip_objects_from_response_by_id,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
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


class CreateApiKey(GenericAPIView):
    """
    Create api key

    This endpoint allows "admin" users to
    create new api keys to access admin endpoints
    """

    serializer_class: Type[Serializer] = CreateApiKeySerializer
    queryset: QuerySet[ApiKey] = ApiKey.objects.all()
    permission_classes = [
        ApiKeyPermission,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_key: ApiKey = ApiKey.objects.create(**serializer.validated_data)
        return Response(
            {
                "value": api_key.value,
                "exprire_time": api_key.expire_time,
            },
            HTTP_201_CREATED,
        )


@method_decorator(
    swagger_auto_schema(manual_parameters=api_keys_list_query_params),
    name="get",
)
class ApiKeysList(ListAPIView):
    """
    Api keys list

    This endpoint allows "admin" users to
    get a list of all the api keys
    """

    serializer_class: Type[Serializer] = ApiKeysListSerializer
    queryset: QuerySet[ApiKey] = ApiKey.get_only_active()
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    search_fields = API_KEYS_LIST_SEARCH_FIELDS
    ordering_fields = API_KEYS_LIST_ORDERING_FIELDS
    permission_classes = [
        ApiKeyPermission,
    ]

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[ApiKey]:
        return self.queryset


class BulkDeleteApiKeys(GenericAPIView):
    """
    Delete api keys

    This endpoint allows the "admin" user to
    delete a certain number of api keys by ID.
    Example:
    {
        "ids": [
            1, 2, 3, 4, 5
        ]
    }
    If the user who sent the request has
    api keys under identifiers: 1,2,3,4,5
    then they will be delete.
    """

    serializer_class: Type[Serializer] = BaseBulkSerializer
    permission_classes = [
        ApiKeyPermission,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = bulk_delete_api_keys(ids=serializer.validated_data["ids"])
        return Response(data, HTTP_200_OK)


class ValidateApiKey(GenericAPIView):
    """
    Validate api key

    This endpoint allows you to check if
    the entered api key is valid or not
    """

    serializer_class: Type[Serializer] = ValidateApiKeySerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_api_key(api_key=serializer.validated_data["value"])
        return Response(API_KEY_IS_VALID_SUCCESS, HTTP_200_OK)
