from typing import Union

from reviews.views import (
    ReviewCreate,
    UserReviewsList,
)

from django.urls import path
from django.urls.resolvers import (
   URLResolver, 
   URLPattern,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    # endpoint where user can create review
    path('client/review/create', ReviewCreate.as_view(), 
        name = 'create-review'),
    # endpoint where user can check her reviews list
    path('client/my/reviews/list', UserReviewsList.as_view(), 
        name = 'reviews-list'),
]