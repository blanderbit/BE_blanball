import re
from collections import OrderedDict
from typing import Any, List, Union

from authentication.constants.code_types import (
    ACCOUNT_DELETE_CODE_TYPE,
    EMAIL_CHANGE_CODE_TYPE,
    EMAIL_VERIFY_CODE_TYPE,
    PASSWORD_CHANGE_CODE_TYPE,
    PASSWORD_RESET_CODE_TYPE,
)
from authentication.constants.errors import (
    CONFIGURATION_IS_REQUIRED_ERROR,
    GET_PLANNED_EVENTS_ERROR,
    INVALID_CREDENTIALS_ERROR,
    PASSWORDS_DO_NOT_MATCH_ERROR,
)
from authentication.models import Profile, User
from authentication.validators import (
    CodeValidator,
)
from cities.serializers import PlaceSerializer
from config.exceptions import _404
from django.contrib import auth
from rest_framework.serializers import (
    BooleanField,
    CharField,
    EmailField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


class UserPublicProfilePlaceSerializer(Serializer):
    place_name: str = CharField(max_length=255)

    class Meta:
        fields = [
            "place_name",
        ]


class ReviewAuthorProfileSerializer(ModelSerializer):
    class Meta:
        model: User = Profile
        fields: Union[str, list[str]] = [
            "name",
            "last_name",
        ]


class ReviewAuthorSerializer(ModelSerializer):
    profile = ReviewAuthorProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = ["id", "profile"]


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields: list[str] = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are specified in the `fields` argument.
            existing = set(fields)
            for field_name in existing:
                self.fields.pop(field_name)


class EventUsersProfileSerializer(ModelSerializer):
    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "name",
            "last_name",
            "avatar_url",
            "position",
            "working_leg",
        ]


class EventAuthorProfileSerializer(ModelSerializer):
    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "last_name",
            "avatar_url",
        ]


class EventAuthorSerializer(ModelSerializer):
    profile = EventAuthorProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "phone",
            "profile",
        ]


class EventUsersSerializer(ModelSerializer):
    profile = EventUsersProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "raiting",
            "profile",
        ]


class FriendProfileSerializer(ModelSerializer):
    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "last_name",
            "avatar_url",
        ]


class FriendUserSerializer(ModelSerializer):
    profile = FriendProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "profile",
            "is_online"
        ]


class ProfileSerializer(ModelSerializer):
    place = UserPublicProfilePlaceSerializer()

    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "last_name",
            "gender",
            "birthday",
            "avatar_url",
            "age",
            "place",
            "height",
            "weight",
            "position",
            "created_at",
            "about_me",
            "working_leg",
        ]


class CreateProfileSerializer(ModelSerializer):
    place = PlaceSerializer(required=False, allow_null=True)

    class Meta:
        model: Profile = Profile
        exclude: Union[str, list[str]] = [
            "created_at",
            "age",
            "coordinates",
            "avatar",
        ]


class UpdateProfileSerializer(ModelSerializer):
    place = PlaceSerializer(required=False, allow_null=True)

    class Meta:
        model: Profile = Profile
        exclude: Union[str, list[str]] = [
            "created_at",
            "age",
            "coordinates",
            "avatar",
        ]


class UserConfigurationSerializer(Serializer):
    email: bool = BooleanField()
    phone: bool = BooleanField()
    show_reviews: bool = BooleanField()

    class Meta:
        fields: Union[str, list[str]] = [
            "email",
            "phone",
            "show_reviews",
        ]


class UpdateUserProfileSerializer(ModelSerializer):
    profile = UpdateProfileSerializer()
    configuration = UserConfigurationSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "get_planned_events",
            "configuration",
            "profile",
            "phone",
        ]

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        conf: str = attrs.get("configuration")
        keys: list[str] = ["email", "phone", "show_reviews"]
        try:
            planned_events = attrs.get("get_planned_events")
            string: str = re.findall(r"\D", planned_events)[0]
            if string not in ["d", "m", "y"]:
                raise ValidationError(GET_PLANNED_EVENTS_ERROR, HTTP_400_BAD_REQUEST)
            if sorted(conf) != sorted(keys):
                raise ValidationError(
                    CONFIGURATION_IS_REQUIRED_ERROR, HTTP_400_BAD_REQUEST
                )
        except TypeError:
            pass

        return super().validate(attrs)

    def update(self, instance, validated_data) -> OrderedDict:
        return super().update(instance, validated_data)


class UpdateUserProfileImageSerializer(ModelSerializer):
    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "avatar",
        ]


class RegisterSerializer(ModelSerializer):

    password: str = CharField(max_length=68, min_length=8, write_only=True)
    re_password: str = CharField(max_length=68, min_length=8, write_only=True)
    profile: Profile = CreateProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "email",
            "phone",
            "password",
            "re_password",
            "profile",
        ]

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        password: str = attrs.get("password", "")
        re_password: str = attrs.get("re_password", "")

        if password != re_password:
            raise ValidationError(PASSWORDS_DO_NOT_MATCH_ERROR, HTTP_400_BAD_REQUEST)
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        validated_data.pop("re_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(ModelSerializer):

    email: str = EmailField(min_length=3, max_length=255)
    password: str = CharField(min_length=8, max_length=68, write_only=True)

    tokens = SerializerMethodField()

    def get_tokens(self, obj) -> dict[str, str]:
        user: User = User.get_all().get(email=obj["email"])
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "email",
            "password",
            "tokens",
        ]

    def validate(
        self, attrs: OrderedDict
    ) -> Union[ValidationError, dict[str, str], OrderedDict]:
        """data validation function for user authorization"""
        email: str = attrs.get("email", "")
        password: str = attrs.get("password", "")
        user: User = auth.authenticate(email=email, password=password)
        if not user:
            raise ValidationError(INVALID_CREDENTIALS_ERROR, HTTP_400_BAD_REQUEST)
        return {"email": user.email, "tokens": user.tokens}

        return super().validate(attrs)


class UserSerializer(DynamicFieldsModelSerializer):

    profile: Profile = ProfileSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "email",
            "role",
            "phone",
            "is_verified",
            "is_online",
            "raiting",
            "configuration",
            "profile",
        ]


class ProfileListSerializer(ModelSerializer):
    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "last_name",
            "avatar_url",
            "position",
            "gender",
            "age",
        ]


class UsersListSerializer(ModelSerializer):
    profile = ProfileListSerializer()

    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "id",
            "raiting",
            "role",
            "is_online",
            "profile",
        ]


class ProfileListDetailSerializer(ModelSerializer):
    class Meta:
        model: Profile = Profile
        fields: Union[str, list[str]] = [
            "id",
            "name",
            "last_name",
            "gender",
            "birthday",
            "age",
            "height",
            "weight",
            "position",
            "created_at",
            "about_me",
            "working_leg",
            "avatar_url",
            "place",
        ]


class UsersListDetailSerializer(ModelSerializer):
    profile = ProfileListDetailSerializer()

    class Meta:
        model: User = User
        exclude: Union[str, list[str]] = [
            "password",
        ]


class EmailSerializer(Serializer):
    email: str = EmailField(min_length=3, max_length=255)

    class Meta:
        fields: Union[str, list[str]] = [
            "email",
        ]


class RequestChangePasswordSerializer(Serializer):
    new_password: str = CharField(min_length=8, max_length=68)
    old_password: str = CharField(min_length=8, max_length=68)

    class Meta:
        fields: Union[str, list[str]] = [
            "new_password",
            "old_password",
        ]


class ResetPasswordSerializer(Serializer):
    new_password: str = CharField(min_length=8, max_length=68, write_only=True)
    verify_code: str = CharField(min_length=5, max_length=5, write_only=True)

    class Meta:
        validators = [CodeValidator(token_type=PASSWORD_RESET_CODE_TYPE)]
        fields: Union[str, list[str]] = [
            "verify_code",
            "new_password",
        ]


class ValidateResetPasswordCodeSerializer(Serializer):
    verify_code: str = CharField(min_length=5, max_length=5, write_only=True)

    class Meta:
        validators = [CodeValidator(token_type=PASSWORD_RESET_CODE_TYPE)]
        fields: Union[str, list[str]] = [
            "verify_code",
        ]


class ValidatePhoneByUniqueSerializer(ModelSerializer):
    class Meta:
        model: User = User
        fields: Union[str, list[str]] = [
            "phone",
        ]


class CheckCodeSerializer(Serializer):
    verify_code: str = CharField(min_length=5, max_length=5, write_only=True)

    class Meta:
        validators = [
            CodeValidator(
                token_type=[
                    PASSWORD_CHANGE_CODE_TYPE,
                    EMAIL_CHANGE_CODE_TYPE,
                    EMAIL_VERIFY_CODE_TYPE,
                    ACCOUNT_DELETE_CODE_TYPE,
                ]
            )
        ]
        fields: Union[str, list[str]] = [
            "verify_code",
        ]


class CheckUserActiveSerializer(Serializer):
    user_id: int = IntegerField(min_value=0)

    class Meta:
        fields: Union[str, list[str]] = [
            "user_id",
        ]

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        user_id: int = attrs.get("user_id")
        try:
            User.get_all().get(id=user_id)
            return super().validate(attrs)
        except User.DoesNotExist:
            raise _404(object=User)
