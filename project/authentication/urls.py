from typing import Union

from authentication.views import (
    CheckCode,
    LoginUser,
    RegisterUser,
    RequestChangePassword,
    RequestChangePhone,
    RequestEmailVerify,
    RequestPasswordReset,
    RequetChangeEmail,
    ResetPassword,
    UpdateProfile,
    UserOwnerProfile,
    UserProfile,
    UsersList,
    UsersRelevantList,
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("client/register", RegisterUser.as_view(), name="register"),
    path("client/login", LoginUser.as_view(), name="login"),
    path("client/users/list", UsersList.as_view(), name="users-list"),
    path(
        "client/users/relevant/list",
        UsersRelevantList.as_view(),
        name="users-relevant-list",
    ),
    path("client/me", UserOwnerProfile.as_view(), name="my-profile"),
    path("client/profile/<int:pk>", UserProfile.as_view(), name="user-profile"),
    path(
        "client/request-reset/password",
        RequestPasswordReset.as_view(),
        name="request-reset-password",
    ),
    path(
        "client/password/reset-complete",
        ResetPassword.as_view(),
        name="complete-reset-password",
    ),
    path(
        "client/request-change/password",
        RequestChangePassword.as_view(),
        name="request-change-password",
    ),
    path("client/check/code", CheckCode.as_view(), name="check-code"),
    path("client/me/update", UpdateProfile.as_view(), name="update-my-profile"),
    path(
        "client/request-change/email",
        RequetChangeEmail.as_view(),
        name="request-change-email",
    ),
    path(
        "client/request-change/phone",
        RequestChangePhone.as_view(),
        name="request-change-phone",
    ),
    path(
        "client/request-verify/email",
        RequestEmailVerify.as_view(),
        name="request-email-verify",
    ),
]
