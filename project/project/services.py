from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from authentication.tasks import Util
import random
import string
from authentication.models import Code
from .constaints import  CODE_EXPIRE_MINUTES_TIME
from django.utils import timezone

def code_create(email,k,type):
    '''create email verification code  and password 
    reset verification code'''
    verify_code = ''.join(random.choices(string.ascii_uppercase, k=k))
    code = Code.objects.create(value = verify_code,user_email = email,type = type,life_time =timezone.now() + 
            timezone.timedelta(minutes=CODE_EXPIRE_MINUTES_TIME))
    print(code.value)
    data = {'email_subject': 'Your verify code','email_body': verify_code ,'to_email': email}
    Util.send_email.delay(data)

class GetPutDeleteAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    '''сoncrete view for get,put or deleting a model instance'''
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PutAPIView(mixins.UpdateModelMixin,
                    GenericAPIView):
    '''concrete view for put a model instance'''
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)