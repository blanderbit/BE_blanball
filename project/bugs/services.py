from authentication.models import User
from bugs.models import Bug


def bulk_delete_bugs(*, ids: dict[str, int], user: User):
    for bug_id in ids:
        try:
            bug = Bug.objects.get(id=bug_id)
            if bug.author == user:
                bug.delete()
                yield bug_id
        except Bug.DoesNotExist:
            pass
