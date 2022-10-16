from typing import Type

from reviews.serializers import (
    CreateReviewSerializer,
    ReviewListSerializer,
)
from reviews.models import (
    Review,
)

from django.db.models.query import QuerySet

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.serializers import (
    Serializer,
)



class ReviewCreate(CreateAPIView):
    serializer_class: Type[Serializer] = CreateReviewSerializer
    queryset: QuerySet[Review] = Review.objects.all().select_related('user')

class UserReviewsList(ListAPIView):
    serializer_class: Type[Serializer] =  ReviewListSerializer
    queryset: QuerySet[Review]  = Review.objects.all().select_related('user')

    def get_queryset(self) -> QuerySet[Review]:
        return self.queryset.filter(user = self.request.user.id).order_by('-time_created')
