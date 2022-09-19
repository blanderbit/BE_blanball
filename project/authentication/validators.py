from .models import Code
from project.constaints import *
from collections import OrderedDict
from django.utils import timezone

from rest_framework import status,serializers



class CodeValidator:
    def __init__(self,token_type:str) -> None:
        self.token_type = token_type

    def __call__(self, attrs) -> OrderedDict:
        self.verify_code = attrs.get('verify_code')
        print(self.verify_code)
        self.code = Code.objects.filter(verify_code = self.verify_code)
        if not self.code:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(verify_code = self.verify_code).type not in self.token_type:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(verify_code = self.verify_code).life_time < timezone.now():
            raise serializers.ValidationError(CODE_EXPIRED_ERROR,status.HTTP_400_BAD_REQUEST)
        return attrs
