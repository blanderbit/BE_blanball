import threading
from typing import Any, final

from authentication.constants.success import (
    BLANBALL,
)
from config.celery import app
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils import timezone
from notifications.models import Notification

from .models import Code, Profile


class EmailThread(threading.Thread):
    def __init__(self, email: str) -> None:
        self.email: str = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


@final
class Util:
    @staticmethod
    @app.task(
        ignore_result=True,
        time_limit=5,
        soft_time_limit=3,
        default_retry_delay=5,
    )
    def send_email(*, data: dict[str, Any]) -> None:
        send: EmailMessage = EmailMessage(
            subject=BLANBALL, body=data["email_body"], to=[data["to_email"]]
        )
        send.content_subtype = "html"
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


@app.task(
    ignore_result=True,
    default_retry_delay=5,
)
def update_user_messages_after_change_avatar(*, profile: Profile) -> None:
    for notification in Notification.get_all().filter(
        Q(data__recipient__id=profile.id) | Q(data__sender__id=profile.id)
    ):
        if profile.id == notification.data["recipient"]["id"]:
            notification.data["recipient"]["avatar"] = profile.avatar_url
            notification.save()
        elif profile.id == notification.data["sender"]["id"]:
            notification.data["sender"]["avatar"] = profile.avatar_url
            notification.save()
