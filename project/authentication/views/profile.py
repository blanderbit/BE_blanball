# ==============================================================================
# profile.py file which includes all controllers responsible for working
# with user profile, get profile, update profile, upload images, update
# uploaded image
# ==============================================================================
from typing import Any, Type

from api_keys.permissions import ApiKeyPermission
from authentication.constants.code_types import (
    ACCOUNT_DELETE_CODE_TYPE,
)
from authentication.constants.success import (
    PROFILE_AVATAR_UPDATED_SUCCESS,
    SENT_CODE_TO_EMAIL_SUCCESS,
)
from authentication.models import User
from authentication.serializers import (
    UpdateUserProfileImageSerializer,
    UpdateUserProfileSerializer,
    UserSerializer,
)
from authentication.services import (
    code_create,
    profile_update,
    update_profile_avatar,
)
from config.exceptions import _404
from django.db import transaction
from django.db.models.query import QuerySet
from django.utils.decorators import (
    method_decorator,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK


class UserOwnerProfile(GenericAPIView):

    serializer_class: Type[Serializer] = UserSerializer

    @swagger_auto_schema(
        tags=["profile"],
    )
    def get(self, request: Request) -> Response:
        """
        User personal profile

        This endpoint allows an authorized user to
        get detailed information about their profile,
        """
        user: User = User.objects.get(id=self.request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(
        tags=["profile"],
    )
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


@method_decorator(
    swagger_auto_schema(
        tags=["profile"],
    ),
    name="put",
)
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


@method_decorator(
    swagger_auto_schema(
        tags=["profile"],
    ),
    name="put",
)
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
        update_profile_avatar(user=user, data=serializer.validated_data)
        return Response(PROFILE_AVATAR_UPDATED_SUCCESS, status=HTTP_200_OK)


@method_decorator(
    swagger_auto_schema(
        tags=["profile", "users"],
    ),
    name="get",
)
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

    permission_classes = [ApiKeyPermission | IsAuthenticated]

    def get(self, request: Request, pk: int) -> Response:
        fields: list[str] = []
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
        except KeyError:
            return Response(serializer.data, status=HTTP_200_OK)
