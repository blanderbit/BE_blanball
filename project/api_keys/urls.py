from typing import Union

from api_keys.views import (
    CreateApiKey,
    ApiKeysList,
    BulkDeleteApiKeys,
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("admin/create/api-key", CreateApiKey.as_view(), name="create-api-key"),
    path("admin/api-keys/list", ApiKeysList.as_view(), name="api-keys-list"),
    path("admin/delete/api-keys", BulkDeleteApiKeys.as_view(), name="delete-api-keys"),
]