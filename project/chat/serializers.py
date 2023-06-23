from typing import Any, List, Union

from authentication.models import (
    User,
    Profile
)
from authentication.serializers import (
    CommonUserProfileSerializer
)
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ListField,
    Serializer,
    ModelSerializer,
    BooleanField,
    ValidationError,
)

READ_OR_UNREAD_MESSAGE_CHOICES: tuple[tuple[str]] = (("read", "read"), ("unread", "unread"))
SER_OR_UNSET_ADMIM_CHOICES: tuple[tuple[str]] = (("set", "set"), ("unset", "unset"))


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


class CreateMessageSerializer(Serializer):

    text: str = CharField(max_length=500)
    chat_id: int = IntegerField(min_value=1)
    reply_to_message_id: int = IntegerField(min_value=1, required=False)

    class Meta:
        fields: Union[str, list[str]] = [
            "text",
            "chat_id",
            "reply_to_message_id"
        ]


class RemoveUserFromChatSerializer(Serializer):

    chat_id: int = IntegerField(min_value=1)
    user_id: int = IntegerField(min_value=1)

    class Meta:
        fields: Union[str, list[str]] = ["chat_id", "user_id"]


class DeleteChatSerializer(Serializer):

    chat_id: int = IntegerField(min_value=1)

    class Meta:
        fields: Union[str, list[str]] = ["chat_id"]


class NewChatDataSerializer(Serializer):
    name: str = CharField(max_length=255, required=False)

    class Meta:
        fields: Union[str, list[str]] = ["name"]


class EditChatSerializer(Serializer):

    chat_id: int = IntegerField(min_value=1)
    new_data: dict[str, str] = NewChatDataSerializer()

    class Meta:
        fields: Union[str, list[str]] = ["chat_id", "new_data"]


class NewChatMessageDataSerializer(Serializer):
    text: str = CharField(max_length=500, required=False)

    class Meta:
        fields: Union[str, list[str]] = ["text"]


class EditChatMessageSerializer(Serializer):

    message_id: int = IntegerField(min_value=1)
    new_data: dict[str, str] = NewChatMessageDataSerializer()

    class Meta:
        fields: Union[str, list[str]] = ["message_id", "new_data"]


class ReadOrUnreadMessagesSerializer(Serializer):
    message_ids: list[int] = ListField(child=IntegerField(min_value=0))
    action: str = ChoiceField(choices=READ_OR_UNREAD_MESSAGE_CHOICES)

    class Meta:
        fields: Union[str, list[str]] = ["message_ids", "action"]


class DeleteMessagesSerializer(Serializer):
    message_ids: list[int] = ListField(child=IntegerField(min_value=0))

    class Meta:
        fields: Union[str, list[str]] = ["message_ids"]


class SetChatAdminSerializer(Serializer):
    user_id: int = IntegerField(min_value=1)
    chat_id: int = IntegerField(min_value=1)
    action: str = ChoiceField(choices=SER_OR_UNSET_ADMIM_CHOICES)

    class Meta:
        fields: Union[str, list[str]] = [
            "user_id",
            "chat_id",
            "action"
        ]


class ChatUserProfileSerializer(CommonUserProfileSerializer):
    def to_representation(self, value):
        return dict(super().to_representation(value))


class ChatUserSerializer(ModelSerializer):
    profile: Profile = ChatUserProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "role",
            "is_online",
            "profile",
        ]

    def to_representation(self, value):
        return dict(super().to_representation(value))


class GetChatUsersListSerializer(Serializer):
    author: bool = BooleanField()
    disabled: bool = BooleanField()
    removed: bool = BooleanField()
    admin: bool = BooleanField()
    chat_deleted: bool = BooleanField()
    user_data: User = ChatUserSerializer(read_only=True)

    class Meta:
        fields: Union[str, list[str]] = [
            "author",
            "disabled",
            "removed",
            "admin",
            "chat_deleted",
            "user_data"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        users_list = self.context.get("users_list")
        if users_list:
            for user in users_list:
                serializer = ChatUserSerializer(user)
                user_data = serializer.data
                data['user_data'] = user_data
        return data
