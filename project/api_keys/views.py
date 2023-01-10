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
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from api_keys.serializers import (
    CreateApiKeySerializer,
    ApiKeysListSerializer,
)
from api_keys.models import (
    ApiKey
)
from api_keys.filters import (
    API_KEYS_LIST_ORDERING_FIELDS,
    API_KEYS_LIST_SEARCH_FIELDS,
)
from api_keys.openapi import api_keys_list_query_params
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from events.services import (
    skip_objects_from_response_by_id,
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


    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[ApiKey]:
        return self.queryset