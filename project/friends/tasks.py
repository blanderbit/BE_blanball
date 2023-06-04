from config.celery import celery
from django.utils import timezone
from friends.models import InviteToFriends


@celery.task
def remove_expired_invitations_to_friends() -> None:
    InviteToFriends.objects.filter(
        status=InviteToFriends.Status.WAITING,
        time_created__lte=timezone.now() - timezone.timedelta(days=30)
    ).delete()
