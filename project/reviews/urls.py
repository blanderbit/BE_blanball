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
    CreateEventReview,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/review/create", ReviewCreate.as_view(), name="create-review"),
    path("client/review/event/review/create", CreateEventReview.as_view(), name="create-event-review"),
    path("client/my/reviews/list", MyReviewsList.as_view(), name="my-reviews-list"),
    path(
        "client/user/reviews/list/<int:pk>",
        UserReviewsList.as_view(),
        name="user-reviews-list",
    ),
]
