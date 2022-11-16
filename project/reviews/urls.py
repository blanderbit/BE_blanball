from typing import Union

from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)
from reviews.views import (
    ReviewCreate,
    UserReviewsList,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/review/create", ReviewCreate.as_view(), name="create-review"),
    path("client/my/reviews/list", UserReviewsList.as_view(), name="reviews-list"),
]
