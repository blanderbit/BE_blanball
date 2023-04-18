from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    TypeVar,
    Union,
)
from friends.models import (
    InviteToFriends,
    Friend
)
from authentication.models import (
    User
)
from rest_framework.serializers import (
    ValidationError,
)


bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])

def invite_users_to_friends(*, users_ids: list[int], request_user: User) -> bulk:
    for user_id in users_ids:
        try:
            invite_user: User = User.get_all().get(id=user_id)
            InviteToFriends.objects.send_invite(
                request_user=request_user, invite_user=invite_user,
            )
            yield {"success": invite_user.id}
        except User.DoesNotExist:
            pass
        except ValidationError:
            pass


def bulk_accept_or_decline_invitions_to_friends(
    *, data: dict[str, Union[list[int], bool]], request_user: User
) -> bulk:
    for invite_id in data["ids"]:
        try:
            invite: InviteToFriends = InviteToFriends.get_all().get(id=invite_id)
            if invite.recipient == request_user and invite.status == invite.Status.WAITING: 
                if data["type"] == True:
                    invite.status = invite.Status.ACCEPTED
                    Friend.objects.create(user=invite.recipient, friend=invite.sender)
                    Friend.objects.create(user=invite.sender, friend=invite.recipient)
                else:
                    invite.status = invite.Status.DECLINED
                invite.save()
                yield {"success": invite_id}
        except InviteToFriends.DoesNotExist:
            pass
