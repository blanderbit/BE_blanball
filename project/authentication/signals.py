from typing import Any, Union

from authentication.models import User
from django.db.models.signals import (
    pre_delete,
)
from django.dispatch import receiver
from authentication.tasks import delete_old_user_profile_avatar


@receiver(pre_delete, sender=User)
def delete_user_avatar_from_storage(sender: User, instance: User, **kwargs) -> None:
    delete_old_user_profile_avatar.delay(profile_id=instance.profile.id)