from reviews.models import Review
from authentication.models import User
from project.constaints import REVIEW_CREATE_ERROR,REVIEW_CREATE_MESSAGE_TYPE
from notifications.tasks import send_to_user
from collections import OrderedDict

from rest_framework import serializers,status



class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('email',)

    def validate(self, attrs) -> OrderedDict:
        user:User = attrs.get('user')
    
        if self.context['request'].user.email == user.email:
            raise serializers.ValidationError(REVIEW_CREATE_ERROR,status.HTTP_400_BAD_REQUEST) 
        return attrs

    def create(self,validated_data:dict[str,any]) -> Review:
        user:User = User.objects.get(email = validated_data['user'])
        send_to_user(user=validated_data['user'],notification_text="Review Create",
        message_type=REVIEW_CREATE_MESSAGE_TYPE)
        review:Review = Review.objects.create(email = self.context['request'].user.email,**validated_data)
        user:User = User.objects.get(email = validated_data['user'])
        for item in user.reviews.all():
            stars = item.stars
        user.raiting = stars / user.reviews.count()
        user.save()
        return review


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text',)