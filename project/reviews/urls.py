from .views import *

from django.urls import path



urlpatterns = [
   # endpoint where the user can create review
    path('client/review/create', ReviewCreate.as_view()),
     # endpoint where client can check her reviews list
    path('client/my/reviews/list', UserReviewsList.as_view()),
    # endpoint where client can update her reviews
    path('client/review/<int:pk>', GetPutDeleteReview.as_view()),
]
