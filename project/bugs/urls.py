from typing import Union

from bugs.views import  (
    CreateBug,
    BugsList,
)


from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/create/bug", CreateBug.as_view(), name="create-bug"),
    path("client/bugs/list", BugsList.as_view(), name="bugs-list")
]
