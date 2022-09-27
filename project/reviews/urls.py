from .views import *

from django.urls import path



urlpatterns = [
    # endpoint where user can create review
    path('client/review/create', ReviewCreate.as_view(),name='create-review'),
    # endpoint where user can check her reviews list
    path('client/my/reviews/list', UserReviewsList.as_view(),name='reviews-list'),
]
