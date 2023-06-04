import threading
from typing import Any, final

from authentication.constants.success import (
    BLANBALL,
)
from authentication.models import Code, Profile
from config.celery import celery
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.encoding import smart_bytes
from django.utils.http import (
    urlsafe_base64_encode,
)
from minio import Minio
from minio.deleteobjects import DeleteObject


class EmailThread(threading.Thread):
    def __init__(self, email: str) -> None:
        self.email: str = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


@final
class Util:
    @staticmethod
    @celery.task(
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


@celery.task
def delete_expire_codes() -> None:
    Code.get_only_expired().delete()


@celery.task
def check_user_age() -> None:
    for user_profile in Profile.objects.all():
        if user_profile.birthday != None:
            rdelta = relativedelta(timezone.now().date(), user_profile.birthday)
            if rdelta.months == 0 and rdelta.days == 0:
                user_profile.age += 1
                user_profile.save()


@celery.task(
    ignore_result=True,
    default_retry_delay=5,
)
def delete_old_user_profile_avatar(*, profile_id: int) -> None:
    client: Minio = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False,
    )
    delete_object_list = map(
        lambda x: DeleteObject(x.object_name),
        client.list_objects(
            settings.MINIO_MEDIA_FILES_BUCKET,
            prefix=f"users/{urlsafe_base64_encode(smart_bytes(profile_id))}",
            recursive=True,
        ),
    )
    errors = client.remove_objects(
        settings.MINIO_MEDIA_FILES_BUCKET, delete_object_list
    )
    for error in errors:
        pass
