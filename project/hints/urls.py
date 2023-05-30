from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from hints.views import HintsList

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/hints/list", HintsList.as_view(), name="hints-list"),
]
