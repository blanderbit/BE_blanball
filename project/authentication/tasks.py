from django.core.mail import EmailMessage
import threading
from .models import Code
from django.utils import timezone
from project.celery import app

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util: 
    @staticmethod
    @app.task
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()



@app.task
def delete_expire_codes():
    for code in Code.objects.all():
        if code.life_time < timezone.now():
            code.delete()
