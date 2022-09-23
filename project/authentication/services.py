from datetime import date
from types import NoneType
import threading
from django.utils import timezone
from .models import *
from django.template.loader import render_to_string
from .tasks import Util
import random
import string



class EmailThread(threading.Thread):

    def __init__(self, email:str) -> None:
        self.email:str = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()

def count_age(profile:Profile,data:dict) -> Profile:
    '''calculation of age after registration by the birthday parameter'''
    for item in data:
        if item[0] == 'birthday':
            birthday:date = item[1]
            age:int = (timezone.now().date() - birthday) // timezone.timedelta(days=365)
            profile.age:int = age
            return profile.save()


def send_email_template(user:User,body_title:str,title:str,text:str) -> None:
    '''send html template to email'''
    context = ({'user_name': user.profile.name,'user_last_name':user.profile.last_name,
    'date_time':timezone.now(),'body_title':body_title,'title':title,'text':text})
    message:str = render_to_string('email_confirm.html',context)
    Util.send_email.delay(data = {'email_body':message,'to_email': user.email})


def check_code_type(code:Code) -> str:
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

def code_create(email:str,type:str,dop_info:str) -> None:
    '''create email verification code'''
    verify_code:str = ''.join(random.choices(string.ascii_uppercase, k=Code._meta.get_field('verify_code').max_length))
    code:Code = Code.objects.create(dop_info = dop_info,verify_code = verify_code,user_email = email,type = type,
        life_time = timezone.now() + timezone.timedelta(minutes=CODE_EXPIRE_MINUTES_TIME))
    user:User = User.objects.get(email = email)
    context:dict = ({'title':check_code_type(code),'code': list(code.verify_code),'name':user.profile.name,'surname':user.profile.last_name})
    template:str = render_to_string("email_code.html",context)
    print(verify_code)
    data:dict = {'email_body': template ,'to_email': email}
    Util.send_email.delay(data)