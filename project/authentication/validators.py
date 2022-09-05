from rest_framework import status,serializers
from project.constaints import *
from .models import Code
from django.utils import timezone


class CodeValidator:
    def __init__(self,token_type):
        self.token_type = token_type

    def __call__(self, attrs):
        self.verify_code = attrs.get('verify_code')
        self.code = Code.objects.filter(value = self.verify_code)
        if not self.code:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = self.verify_code).type not in self.token_type:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = self.verify_code).life_time < timezone.now():
            raise serializers.ValidationError(CODE_EXPIRED_ERROR,status.HTTP_400_BAD_REQUEST)
        return attrs