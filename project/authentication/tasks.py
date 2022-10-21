from typing import Any, final
from django.utils import timezone
import threading

from dateutil.relativedelta import relativedelta

from .models import Code,Profile
from project.celery import app

from django.core.mail import EmailMessage

from authentication.constant.success import BLANBALL


class EmailThread(threading.Thread):

    def __init__(self, email: str) -> None:
        self.email: str = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()
        
@final
class Util: 
    @staticmethod
    @app.task
    def send_email(*, data: dict[str, Any]) -> None:
        send: EmailMessage = EmailMessage(
        subject = BLANBALL, body = data['email_body'], to = [data['to_email']])
        send.content_subtype = 'html'
        EmailThread(send).start()


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