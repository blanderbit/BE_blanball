import copy
import random
import string
from datetime import date
from typing import Any

from authentication.constants.code_types import (
    ACCOUNT_DELETE_CODE_TYPE,
    EMAIL_CHANGE_CODE_TYPE,
    EMAIL_VERIFY_CODE_TYPE,
    PASSWORD_CHANGE_CODE_TYPE,
    PASSWORD_RESET_CODE_TYPE,
)
from authentication.constants.success import (
    EMAIL_MESSAGE_TEMPLATE_TITLE,
    TEMPLATE_SUCCESS_BODY_TITLE,
    TEMPLATE_SUCCESS_TEXT,
    TEMPLATE_SUCCESS_TITLE,
)
from authentication.models import (
    Code,
    Profile,
    User,
)
from authentication.tasks import (
    delete_old_user_profile_avatar,
    update_user_messages_after_change_avatar,
)
from django.conf import settings
from django.template.loader import (
    render_to_string,
)
from django.utils import timezone
from minio import Minio
from minio.commonconfig import REPLACE, CopySource
from rest_framework.serializers import Serializer

from .tasks import Util


def count_age(*, profile: Profile, data: dict[str, Any]) -> Profile:
    """calculation of age after registration by the birthday parameter"""
    for item in data:
        if item[0] == "birthday":
            birthday: date = item[1]
            age: int = (timezone.now().date() - birthday) // timezone.timedelta(
                days=365
            )
            profile.age: int = age
            return profile.save()


def send_email_template(*, user: User, body_title: str, title: str, text: str) -> None:
    """send html template to email"""
    context = {
        "user_name": user.profile.name,
        "user_last_name": user.profile.last_name,
        "date_time": timezone.now(),
        "body_title": body_title,
        "title": title,
        "text": text,
    }
    message: str = render_to_string("email_confirm.html", context)
    Util.send_email.delay(data={"email_body": message, "to_email": user.email})


def check_code_type(*, code: Code) -> str:
    if code.type == EMAIL_CHANGE_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type="Change", key="email address")
    elif code.type == ACCOUNT_DELETE_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type="Removal", key="account")
    elif code.type == EMAIL_VERIFY_CODE_TYPE:
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(
            type="Confirmation", key="email address"
        )
    elif code.type in (PASSWORD_CHANGE_CODE_TYPE, PASSWORD_RESET_CODE_TYPE):
        title = EMAIL_MESSAGE_TEMPLATE_TITLE.format(type="Change", key="password")
    return title


def code_create(*, email: str, type: str, dop_info: str) -> None:
    """create email verification code"""
    verify_code: str = "".join(
        random.choices(
            string.ascii_uppercase, k=Code._meta.get_field("verify_code").max_length
        )
    )
    code: Code = Code.objects.create(
        dop_info=dop_info,
        verify_code=verify_code,
        user_email=email,
        type=type,
        life_time=timezone.now()
        + timezone.timedelta(minutes=settings.CODE_EXPIRE_MINUTES_TIME),
    )
    user: User = User.get_all().get(email=email)
    context: dict = {
        "title": check_code_type(code=code),
        "code": list(code.verify_code),
        "name": user.profile.name,
        "surname": user.profile.last_name,
    }
    template: str = render_to_string("email_code.html", context)
    print(verify_code)
    Util.send_email.delay(data={"email_body": template, "to_email": email})


def update_user_profile_avatar(*, avatar, profile_id: int) -> None:
    try:
        profile: Profile = Profile.objects.get(id=profile_id)
        if avatar != None:
            client: Minio = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False,
            )
            client.copy_object(
                settings.MINIO_MEDIA_FILES_BUCKET,
                profile.new_image_name,
                CopySource(settings.MINIO_MEDIA_FILES_BUCKET, avatar.name),
                metadata_directive=REPLACE,
            )
            if avatar.name != profile.new_image_name:
                client.remove_object(settings.MINIO_MEDIA_FILES_BUCKET, avatar.name)
            avatar.name = profile.new_image_name
    except ValueError:
        pass


def profile_update(*, profile_id: int, serializer: Serializer) -> dict[str, Any]:
    profile: Profile = Profile.objects.filter(id=profile_id)
    profile.update(**serializer.validated_data["profile"])
    count_age(profile=profile[0], data=serializer.validated_data["profile"].items())
    result: dict[str, Any] = copy.deepcopy(serializer.validated_data)
    serializer.validated_data.pop("profile")
    serializer.save()
    return result


def update_profile_avatar(*, profile: Profile, data: dict[str, Any]) -> None:
    delete_old_user_profile_avatar.delay(profile_id=profile.id)
    profile.avatar = data.get("avatar")
    if data.get("avatar") != None:
        profile.avatar.name: str = profile.new_image_name.replace("users/", "")
    profile.save()
    update_user_messages_after_change_avatar.delay(profile_id=profile.id)


def reset_password(*, data: dict[str, Any]) -> None:
    verify_code: str = data["verify_code"]
    code: Code = Code.objects.get(verify_code=verify_code)
    user: User = User.get_all().get(email=code.user_email)
    user.set_password(data["new_password"])
    user.save()
    code.delete()
    send_email_template(
        user=user,
        body_title=TEMPLATE_SUCCESS_BODY_TITLE.format(key="password"),
        title=TEMPLATE_SUCCESS_TITLE.format(key="password"),
        text=TEMPLATE_SUCCESS_TEXT.format(key="password"),
    )
