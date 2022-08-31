from rest_framework import serializers,status
from .models import *
from project.constaints import REVIEW_CREATE_ERROR
from notifications.tasks import send_to_user

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('email',)

    def validate(self, attrs):
        user = attrs.get('user')
    
        if self.context['request'].user.email == user.email:
            raise serializers.ValidationError(REVIEW_CREATE_ERROR,status.HTTP_400_BAD_REQUEST) 
        return attrs

    def create(self,validated_data):
        send_to_user(user=self.context['request'].user,notification_text="Review Create")
        return Review.objects.create(email = self.context['request'].user.email,**validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('user',)

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text',)