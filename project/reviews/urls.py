from django.urls import path
from .views import *



urlpatterns = [
   # endpoint where the user can create review
    path('client/review/create', ReviewCreate.as_view(),
      name="review-create"),
     # endpoint where client can check her reviews list
    path('client/my/reviews/list', UserReviewsList.as_view(),
      name="my-reviews"),
    # endpoint where client can update her reviews
    path('client/review/<int:pk>', GetPutDeleteReview.as_view(),
      name="update-review"),
]
