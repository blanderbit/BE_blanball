from typing import Any, Type

from authentication.constants.code_types import (
    ACCOUNT_DELETE_CODE_TYPE,
    EMAIL_CHANGE_CODE_TYPE,
    EMAIL_VERIFY_CODE_TYPE,
    PASSWORD_CHANGE_CODE_TYPE,
    PASSWORD_RESET_CODE_TYPE,
)
from authentication.constants.errors import (
    ALREADY_VERIFIED_ERROR,
    NO_PERMISSIONS_ERROR,
    THIS_EMAIL_ALREADY_IN_USE_ERROR,
    WRONG_PASSWORD_ERROR,
)
from authentication.constants.success import (
    ACCOUNT_DELETE_SUCCESS_BODY_TITLE,
    ACCOUNT_DELETE_SUCCESS_TEXT,
    ACCOUNT_DELETE_SUCCESS_TITLE,
    ACCOUNT_DELETED_SUCCESS,
    ACTIVATION_SUCCESS,
    CHANGE_EMAIL_SUCCESS,
    CHANGE_PASSWORD_SUCCESS,
    EMAIL_VERIFY_SUCCESS_BODY_TITLE,
    EMAIL_VERIFY_SUCCESS_TEXT,
    EMAIL_VERIFY_SUCCESS_TITLE,
    PASSWORD_RESET_SUCCESS,
    PROFILE_AVATAR_UPDATED_SUCCESS,
    REGISTER_SUCCESS_BODY_TITLE,
    REGISTER_SUCCESS_TEXT,
    REGISTER_SUCCESS_TITLE,
    RESET_PASSWORD_CODE_IS_VALID_SUCCESS,
    SENT_CODE_TO_EMAIL_SUCCESS,
    TEMPLATE_SUCCESS_BODY_TITLE,
    TEMPLATE_SUCCESS_TEXT,
    TEMPLATE_SUCCESS_TITLE,
)
from authentication.filters import (
    RankedFuzzySearchFilter,
    UserAgeRangeFilter,
)
from authentication.models import (
    Code,
    Profile,
    User,
)
from authentication.openapi import (
    users_list_query_params,
    users_relevant_list_query_params,
)
from authentication.permisions import (
    IsNotAuthenticated,
)
from authentication.serializers import (
    CheckCodeSerializer,
    EmailSerializer,
    LoginSerializer,
    RegisterSerializer,
    RequestChangePasswordSerializer,
    ResetPasswordSerializer,
    UpdateUserProfileImageSerializer,
    UpdateUserProfileSerializer,
    UserSerializer,
    UsersListSerializer,
    ValidateResetPasswordCodeSerializer,
)
from authentication.services import (
    code_create,
    count_age,
    profile_update,
    reset_password,
    send_email_template,
    update_profile_avatar,
)
from config.exceptions import _404
from django.db import transaction
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from events.services import (
    add_dist_filter_to_view,
    skip_objects_from_response_by_id,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    Serializer,
    ValidationError,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework_gis.filters import (
    DistanceToPointOrderingFilter,
)


class RegisterUser(GenericAPIView):
    """
    Registration

    This endpoint allows any user to register on the site.
    The email and phone number fields are required
    and must be unique!
    The birthday field has some restrictions: the date of
    birth must not be less than 6 years ago and not
    more than 80 years ago.

    List of required fields: "email", "phone", "password",
    "re_password", "name", "last_name", "gender"

    List of optional fields:  "birthday", "height",
    "weight", "position", "about_me", "working_leg",
    "avatar"

    position field options: "GK", "LB", "RB", "CB",
    "LWB", "RWB", "CDM", "CM", "CAM", "RM", "LM", "RF",
    "CF", "LF", "ST"
    working_leg options: "Left", "Right"
    """

    serializer_class: Type[Serializer] = RegisterSerializer
    permission_classes = [
        IsNotAuthenticated,
    ]

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile: Profile = Profile.objects.create(
            **serializer.validated_data["profile"]
        )
        count_age(profile=profile, data=serializer.validated_data["profile"].items())
        serializer.save(profile=profile)
        user: User = User.get_all().get(profile=profile.id)
        send_email_template(
            user=user,
            body_title=REGISTER_SUCCESS_BODY_TITLE,
            title=REGISTER_SUCCESS_TITLE,
            text=REGISTER_SUCCESS_TEXT,
        )
        return Response(
            {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]},
            status=HTTP_201_CREATED,
        )


class LoginUser(GenericAPIView):
    """
    Login

    This endpoint allows a previously
    registered user to log in to the system.
    """

    serializer_class: Type[Serializer] = LoginSerializer
    permission_classes = [
        IsNotAuthenticated,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UserOwnerProfile(GenericAPIView):

    serializer_class: Type[Serializer] = UserSerializer

    def get(self, request: Request) -> Response:
        """
        User personal profile

        This endpoint allows an authorized user to
        get detailed information about their profile,
        """
        user: User = User.get_all().get(id=self.request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        """
        Request delete profile

        This endpoint allows the user to send a
        request to delete their account.
        """
        code_create(
            email=request.user.email,
            type=ACCOUNT_DELETE_CODE_TYPE,
            dop_info=request.user.email,
        )
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=HTTP_200_OK)


class UpdateProfile(GenericAPIView):
    """
    Update profile

    This class allows an authorized
    user to change their profile information.
    """

    serializer_class: Type[Serializer] = UpdateUserProfileSerializer
    queryset: QuerySet[User] = User.get_all()

    @transaction.atomic
    def put(self, request: Request) -> Response:
        user: User = self.queryset.get(id=self.request.user.id)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        result: dict[str, Any] = profile_update(
            profile_id=user.profile_id, serializer=serializer
        )
        return Response(result, status=HTTP_200_OK)


class UpdateProfileImage(GenericAPIView):
    """
    Update profile avatar

    This endpoint allows the user to change
    their profile avatar to any other
    """

    parser_classes = [MultiPartParser]
    serializer_class: Type[Serializer] = UpdateUserProfileImageSerializer
    queryset: QuerySet[User] = User.get_all()

    def put(self, request: Request) -> Response:
        user: User = self.queryset.get(id=self.request.user.id)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        update_profile_avatar(profile=user.profile, data=serializer.validated_data)
        return Response(PROFILE_AVATAR_UPDATED_SUCCESS, status=HTTP_200_OK)


class UserProfile(GenericAPIView):
    """
    User profile

    This class makes it possible to
    get information about any user of the application
    !! It is important that the profile information may differ,
    because information about the phone number and mail may be hidden !!
    """

    serializer_class: Type[Serializer] = UserSerializer
    queryset: QuerySet[User] = User.get_all()

    def get(self, request: Request, pk: int) -> Response:
        fields: list[str] = ["configuration"]
        try:
            user: User = self.queryset.get(id=pk)
            for item in user.configuration.items():
                if item[1] == True:
                    serializer = self.serializer_class(user, fields=(fields))
                elif item[1] == False:
                    fields.append(item[0])
                    serializer = self.serializer_class(user, fields=(fields))
            return Response(serializer.data, status=HTTP_200_OK)
        except User.DoesNotExist:
            raise _404(object=User)


@method_decorator(
    swagger_auto_schema(manual_parameters=users_list_query_params),
    name="get",
)
class UsersList(ListAPIView):
    """
    List of users

    This class makes it possible to
    get a list of all users of the application.
    """

    serializer_class: Type[Serializer] = UsersListSerializer
    queryset: QuerySet[User] = User.get_all()
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
        DistanceToPointOrderingFilter,
    ]
    filterset_class = UserAgeRangeFilter
    ordering_fields: list[str] = ["id", "profile__age", "raiting"]
    search_fields: list[str] = [
        "profile__name",
        "profile__gender",
        "profile__last_name",
    ]
    distance_ordering_filter_field: str = "profile__coordinates"
    distance_filter_convert_meters: bool = True

    @skip_objects_from_response_by_id
    @add_dist_filter_to_view
    def get_queryset(self) -> QuerySet[User]:
        return self.queryset.filter(role="User")


@method_decorator(
    swagger_auto_schema(manual_parameters=users_relevant_list_query_params),
    name="get",
)
class UsersRelevantList(ListAPIView):
    """
    Relevant user search

    This class makes it possible to get the 5 most
    relevant users for a search query.
    """

    filter_backends = [
        RankedFuzzySearchFilter,
    ]
    serializer_class: Type[Serializer] = UsersListSerializer
    queryset: QuerySet[User] = User.get_all()
    search_fields: list[str] = ["profile__name", "profile__last_name"]

    def get_queryset(self) -> QuerySet[User]:
        return UsersList.get_queryset(self)


class RequestPasswordReset(GenericAPIView):
    """
    Request password reset

    This class allows an unauthorized user to
    request a password reset. \nAfter submitting the
    application, a confirmation code will be sent
    to the email specified by the user.
    """

    serializer_class: Type[Serializer] = EmailSerializer
    permission_classes = [
        IsNotAuthenticated,
    ]

    def post(self, request: Request) -> Response:
        email: str = request.data.get("email", "")
        try:
            User.get_all().get(email=email)
            code_create(email=email, type=PASSWORD_RESET_CODE_TYPE, dop_info=None)
            return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=HTTP_200_OK)
        except User.DoesNotExist:
            raise _404(object=User)


class ResetPassword(GenericAPIView):
    """
    Confirm password reset

    This class makes it possible to confirm a password
    reset request using the code that was sent to the
    mail after the request was sent.
    """

    serializer_class: Type[Serializer] = ResetPasswordSerializer
    permission_classes = [
        IsNotAuthenticated,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            reset_password(data=serializer.validated_data)
            return Response(PASSWORD_RESET_SUCCESS, status=HTTP_200_OK)
        except User.DoesNotExist:
            raise _404(object=User)


class ValidateResetPasswordCode(GenericAPIView):
    """
    Validate reset password code

    This endpoint allows the user to check the password reset code for
    validity before using it
    """

    serializer_class: Type[Serializer] = ValidateResetPasswordCodeSerializer
    permission_classes = [
        IsNotAuthenticated,
    ]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(RESET_PASSWORD_CODE_IS_VALID_SUCCESS, HTTP_200_OK)


class RequestChangePassword(GenericAPIView):
    """
    Request change password

    This class allows an authorized user to request a password change.
    After submitting the application, a confirmation code will be sent.
    to the email address provided by the user.
    """

    serializer_class: Type[Serializer] = RequestChangePasswordSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data.get("old_password")):
            return Response(WRONG_PASSWORD_ERROR, status=HTTP_400_BAD_REQUEST)
        code_create(
            email=request.user.email,
            type=PASSWORD_CHANGE_CODE_TYPE,
            dop_info=serializer.validated_data["new_password"],
        )
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=HTTP_200_OK)


class RequestEmailVerify(GenericAPIView):
    """
    Request verify email

    This class allows an authorized user to request account verification.
    After submission, a confirmation code will be sent.
    to the email address provided by the user.

    If the user is already verified, he cannot send a second request
    """

    serializer_class: Type[Serializer] = EmailSerializer

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_verified:
            return Response(ALREADY_VERIFIED_ERROR, status=HTTP_400_BAD_REQUEST)
        code_create(email=user.email, type=EMAIL_VERIFY_CODE_TYPE, dop_info=user.email)
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=HTTP_200_OK)


class RequetChangeEmail(GenericAPIView):
    """
    Request change email

    This class allows an authorized user to request a email change.
    After submitting the application, a confirmation code will be sent.
    to the email address provided by the user.
    """

    serializer_class: Type[Serializer] = EmailSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.get_all().filter(email=serializer.validated_data["email"]):
            code_create(
                email=request.user.email,
                type=EMAIL_CHANGE_CODE_TYPE,
                dop_info=serializer.validated_data["email"],
            )
            return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=HTTP_200_OK)
        return Response(THIS_EMAIL_ALREADY_IN_USE_ERROR, status=HTTP_400_BAD_REQUEST)




class CheckCode(GenericAPIView):
    """
    Сode confirmations

    This endpoint allows the user to:
    confirm changing the password, phone number,
    email, account verification, as well as deleting
    the account using the previously received code
    that comes to the mail
    """

    serializer_class: Type[Serializer] = CheckCodeSerializer

    def success(self, key: str) -> None:
        self.user.save()
        self.code.delete()
        send_email_template(
            user=self.user,
            body_title=TEMPLATE_SUCCESS_BODY_TITLE.format(key=key),
            title=TEMPLATE_SUCCESS_TITLE.format(key=key),
            text=TEMPLATE_SUCCESS_TEXT.format(key=key),
        )

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_code: str = serializer.validated_data["verify_code"]
        self.code: Code = Code.objects.get(verify_code=verify_code)
        self.user: User = User.get_all().get(id=request.user.id)
        if self.code.user_email != self.user.email:
            raise ValidationError(NO_PERMISSIONS_ERROR, HTTP_400_BAD_REQUEST)

        if self.code.type == PASSWORD_CHANGE_CODE_TYPE:
            self.user.set_password(self.code.dop_info)
            self.success(key="password")
            return Response(CHANGE_PASSWORD_SUCCESS, status=HTTP_200_OK)

        elif self.code.type == EMAIL_CHANGE_CODE_TYPE:
            self.user.email = self.code.dop_info
            self.success(key="email")
            return Response(CHANGE_EMAIL_SUCCESS, status=HTTP_200_OK)

        elif self.code.type == ACCOUNT_DELETE_CODE_TYPE:
            send_email_template(
                user=self.user,
                body_title=ACCOUNT_DELETE_SUCCESS_BODY_TITLE,
                title=ACCOUNT_DELETE_SUCCESS_TITLE,
                text=ACCOUNT_DELETE_SUCCESS_TEXT,
            )
            User.get_all().filter(id=self.user.id).delete()
            self.code.delete()
            return Response(ACCOUNT_DELETED_SUCCESS, status=HTTP_200_OK)

        elif self.code.type == EMAIL_VERIFY_CODE_TYPE:
            self.user.is_verified = True
            self.user.save()
            self.code.delete()
            send_email_template(
                user=self.user,
                body_title=EMAIL_VERIFY_SUCCESS_BODY_TITLE,
                title=EMAIL_VERIFY_SUCCESS_TITLE,
                text=EMAIL_VERIFY_SUCCESS_TEXT,
            )
            return Response(ACTIVATION_SUCCESS, status=HTTP_200_OK)
