from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from reviews.views import (
    MyReviewsList,
    ReviewCreate,
    UserReviewsList,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    # endpoint where user can create review
    path("client/review/create", ReviewCreate.as_view(), name="create-review"),
    path("client/my/reviews/list", MyReviewsList.as_view(), name="my-reviews-list"),
    path(
        "client/user/reviews/list/<int:pk>",
        UserReviewsList.as_view(),
        name="user-reviews-list",
    ),
]
