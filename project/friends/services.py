from friends.models import (
    InviteToFriends,
)
from authentication.models import (
    User
)
from rest_framework.serializers import (
    ValidationError,
)

def invite_users_to_friends(*, users_ids: list[int], request_user: User) -> None:
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