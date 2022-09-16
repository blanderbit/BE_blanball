from authentication.tasks import Util
from authentication.models import User,Code
from notifications.tasks import send_to_user
from .constaints import  *

import random
import string

from django.utils import timezone
from django.template.loader import render_to_string

from rest_framework import mixins,response,pagination
from rest_framework.generics import GenericAPIView

def check_code_type(code):
    if code.type == PHONE_CHANGE_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type = 'Зміна',key = 'номеру телефону')
    elif code.type == EMAIL_CHANGE_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type = 'Зміна',key = 'електронної адреси')
    elif code.type == ACCOUNT_DELETE_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type = 'Видалення',key = 'аккаунту')
    elif code.type == EMAIL_VERIFY_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type = 'Підтвердження',key = 'електронної адреси')
    elif code.type in (PASSWORD_CHANGE_CODE_TYPE,PASSWORD_RESET_CODE_TYPE):
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type = 'Зміна',key = 'паролю')
    return title

def code_create(email,type,dop_info):
    '''create email verification code'''
    verify_code = ''.join(random.choices(string.ascii_uppercase, k=Code._meta.get_field('verify_code').max_length))
    code = Code.objects.create(dop_info = dop_info,verify_code = verify_code,user_email = email,type = type,
    life_time = timezone.now() + timezone.timedelta(minutes=CODE_EXPIRE_MINUTES_TIME))
    user = User.objects.get(email = email)
    context = ({'title':check_code_type(code),'code': list(code.verify_code),'name':user.profile.name,'surname':user.profile.last_name})
    template = render_to_string("email_confirm.html",context)
    print(verify_code)
    data = {'email_subject': 'Blanball','email_body': template ,'to_email': email}
    Util.send_email.delay(data)




def send_notification_to_event_author(event):
    if event.amount_members > event.count_current_users:
        user_type = 'новий'
    elif event.amount_members == event.count_current_users:
        user_type = 'останній'
    send_to_user(user = User.objects.get(id = event.author.id),notification_text=
        NEW_USER_ON_THE_EVENT_NOTIFICATION.format(author_name = event.author.profile.name,user_type=user_type,event_id = event.id),
        message_type=NEW_USER_ON_THE_EVENT_MESSAGE_TYPE)


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
    page_size = 10
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
