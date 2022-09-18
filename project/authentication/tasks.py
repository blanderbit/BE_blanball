import threading
from dateutil.relativedelta import relativedelta

from .models import Code,Profile
from project.celery import app

from django.core.mail import EmailMessage
from django.utils import timezone

class EmailThread(threading.Thread):

    def __init__(self, email:str) -> None:
        self.email:str = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


class Util: 
    @staticmethod
    @app.task
    def send_email(data:dict) -> None:
        email:str = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.content_subtype = "html"
        EmailThread(email).start()


@app.task
def delete_expire_codes() -> None:
    for code in Code.objects.all():
        if code.life_time < timezone.now():
            code.delete()

@app.task
def check_user_age() -> None:
    for user_profile in Profile.objects.all():
        rdelta = relativedelta(timezone.now().date(), user_profile.birthday)
        if rdelta.months == 0 and rdelta.days == 0:
            user_profile.age += 1
            user_profile.save()