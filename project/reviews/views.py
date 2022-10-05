from .serializers import *
from .models import *
from project.settings import CustomPagination
from django.db.models.query import QuerySet

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)


class ReviewCreate(CreateAPIView):
    serializer_class = CreateReviewSerializer
    queryset = Review.objects.all().select_related('user')

class UserReviewsList(ListAPIView):
    serializer_class =  ReviewListSerializer
    pagination_class = CustomPagination
    queryset = Review.objects.all().select_related('user')

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(user = self.request.user.id).order_by('-time_created')
