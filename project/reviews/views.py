from typing import Type

from config.openapi import (
    offset_query,
    skip_param_query,
)
from config.pagination import paginate_by_offset
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from events.services import (
    only_for_event_members,
    skip_objects_from_response_by_id,
)
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_201_CREATED
from reviews.constants.success import (
    EVENT_REVIEW_CREATED_SUCCESS,
)
from reviews.models import EventReview, Review
from reviews.serializers import (
    CreateEventReviewSerializer,
    CreateReviewSerializer,
    ReviewListSerializer,
)
from reviews.services import hide_user_reviews


class ReviewCreate(CreateAPIView):
    """
    Create review

    This endpoint gives you the ability
    to set up a review for another user.
    Based on each new review, the recipient's
    rating will be recalculated. The rating is
    calculated using the arithmetic mean formula.
    """

    serializer_class: Type[Serializer] = CreateReviewSerializer
    queryset: QuerySet[Review] = Review.get_all()


@method_decorator(
    swagger_auto_schema(manual_parameters=[skip_param_query, offset_query]), name="get"
)
@paginate_by_offset
class MyReviewsList(ListAPIView):
    """
    List of my reviews

    This endpoint allows the user to
    get a list of reviews left to him.
    """

    serializer_class: Type[Serializer] = ReviewListSerializer
    queryset: QuerySet[Review] = Review.get_all()

    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Review]:
        return self.queryset.filter(user_id=self.request.user.id)


class UserReviewsList(MyReviewsList):
    """
    List of user reviews

    This endpoint makes it possible to
    get a list of reviews of any user,
    if access to them is open.
    """

    @hide_user_reviews
    @skip_objects_from_response_by_id
    def get_queryset(self) -> QuerySet[Review]:
        return self.queryset.filter(user_id=self.kwargs["pk"])


class CreateEventReview(GenericAPIView):
    """
    Create event review

    This endpoint gives you the ability
    to set up a review for some event.
    """

    serializer_class: Type[Serializer] = CreateEventReviewSerializer

    @only_for_event_members
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        EventReview.objects.create(author=request.user, **serializer.validated_data)
        return Response(EVENT_REVIEW_CREATED_SUCCESS, HTTP_201_CREATED)
