from typing import Union

from api_keys.views import (
    CreateApiKey
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("admin/create/api-key", CreateApiKey.as_view(), name="create-api-key"),
]