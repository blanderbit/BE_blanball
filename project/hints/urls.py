from typing import Union

from hints.views import (
    HintsList
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/hints/list", HintsList.as_view(), name="hints-list"),
]
