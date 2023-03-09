from typing import Union

from bugs.views import (
    BugsList,
    BulkDeleteBugs,
    ChangeBugType,
    CreateBug,
    MyBugs,
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/create/bug", CreateBug.as_view(), name="create-bug"),
    path("client/bugs/list", BugsList.as_view(), name="bugs-list"),
    path("client/my/bugs/list", MyBugs.as_view(), name="my-bugs-list"),
    path("client/delete/bugs", BulkDeleteBugs.as_view(), name="delete-bugs"),
    path("client/change/bug/type", ChangeBugType.as_view(), name="change-bug-type"),
]
