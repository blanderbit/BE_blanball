from nis import match
from rest_framework import mixins,response,pagination
from rest_framework.generics import GenericAPIView
from authentication.tasks import Util
import random
import string
from authentication.models import Code
from authentication.models import User
from .constaints import  *
from django.utils import timezone
from django.template.loader import render_to_string


def code_create(email,k,type,dop_info):
    '''create email verification code  and password 
    reset verification code'''
    verify_code = ''.join(random.choices(string.ascii_uppercase, k=k))
    code = Code.objects.create(dop_info = dop_info,value = verify_code,user_email = email,type = type,life_time =timezone.now() + 
            timezone.timedelta(minutes=CODE_EXPIRE_MINUTES_TIME))
    user = User.objects.get(email = email)
    if code.type == PHONE_CHANGE_CODE_TYPE:
        title = 'Зміна номеру телефону у додатку BlanBall'
    elif code.type == EMAIL_CHANGE_CODE_TYPE:
        title = 'Зміна електронної адреси у додатку Blanball'
    elif code.type == EMAIL_VERIFY_CODE_TYPE:
        title = 'Підтвердження електронної адреси у додатку Blanball'
    elif code.type in [PASSWORD_CHANGE_CODE_TYPE,PASSWORD_RESET_CODE_TYPE]:
        title = 'Зміна паролю у додатку Blanball'
    context = ({'title':title,'code': list(code.value),'name':user.profile.name,'surname':user.profile.last_name})
    template = render_to_string("email_confirm.html",context)
    data = {'email_subject': 'Blanball','email_body': template ,'to_email': email}
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



class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return response.Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
