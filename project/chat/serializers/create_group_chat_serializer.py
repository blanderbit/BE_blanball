from typing import Union

from authentication.models import User
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    Serializer,
    ValidationError,
)


class CreateGroupChatSerializer(Serializer):

    name: str = CharField(max_length=255)
    users: list[int] = ListField(child=IntegerField(min_value=1), allow_empty=True)

    class Meta:
        fields: Union[str, list[str]] = ["name", "users"]

    def validate(self, attrs):
        user_ids = set(attrs.get("users", []))
        existing_users = User.objects.filter(id__in=user_ids)

        existing_user_ids = set(user.id for user in existing_users)
        non_existing_user_ids = user_ids - existing_user_ids

        # if self.context["request"].user.id in existing_user_ids:
        #     raise ValidationError(
        #         f"Users with IDs {non_existing_user_ids} do not exist."
        #     )

        if non_existing_user_ids:
            raise ValidationError(
                f"Users with IDs {non_existing_user_ids} do not exist."
            )

        return super().validate(attrs)
