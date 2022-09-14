from .views import *

from django.urls import path



urlpatterns = [
    # endpoint where user can create review
    path('client/review/create', ReviewCreate.as_view(),name='create-review'),
    # endpoint where user can check her reviews list
    path('client/my/reviews/list', UserReviewsList.as_view(),name='reviews-list'),
    # endpoint where user can update her reviews
    path('client/review/<int:pk>', GetPutDeleteReview.as_view(),name='get-put-delete-review'),
]
