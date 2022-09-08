from .serializers import *
from .models import *
from project.services import CustomPagination,GetPutDeleteAPIView

from rest_framework import generics,permissions,response,status


class ReviewCreate(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

class UserReviewsList(generics.ListAPIView):
    serializer_class =  ReviewListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Review.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user_id = self.request.user).order_by('-time_created')


class GetPutDeleteReview(GetPutDeleteAPIView):
    serializer_class =  ReviewUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()