from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from authentication.tasks import Util
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_encode
import random
import string
from authentication.models import Code ,User

def code_create(email,k,type):
    user = User.objects.get(email=email)
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            
    uidb64 += ''.join(random.choices(string.ascii_uppercase, k=k))
    print(uidb64)
    Code.objects.create(value = uidb64,user = User.objects.get(email=email),type = type)

    data = {'email_body': uidb64 ,'to_email': email, 
            'email_subject': 'Your verify code'}
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