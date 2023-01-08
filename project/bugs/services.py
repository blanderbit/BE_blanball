from typing import Any

from authentication.models import User
from bugs.models import Bug, BugImage


def bulk_delete_bugs(*, ids: dict[str, int], user: User):
    for bug_id in ids:
        try:
            bug = Bug.objects.get(id=bug_id)
            if bug.author == user:
                bug.delete()
                yield bug_id
        except Bug.DoesNotExist:
            pass


def create_bug(validated_data: dict[str, Any], request_user: User) -> None:
    try:
        images = validated_data.get("images")
        validated_data.pop("images")

        images_list = []
        for image in images:
            images_list.append(BugImage(image=image))
        if images_list:
            bug: Bug = Bug.objects.create(author=request_user, **validated_data)
            bug.images.set(BugImage.objects.bulk_create(images_list))
    except KeyError:
        bug: Bug = Bug.objects.create(author=request_user, **validated_data)
