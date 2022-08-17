from .views import *
from django.urls import path


urlpatterns = [
    # endpoint where the user can create an account
    path('client/register', RegisterUser.as_view(), name="register"),
    # endpoint where the user can log into a previously created account
    path('client/login', LoginUser.as_view(), name="login"),
    # endpoint where admin can check all users list
    path('admin/user/list',UserList.as_view(),
      name = 'users-list'),
    # endpoint where admin can check all admins list
    path('admin/list',AdminUsersList.as_view(),
        name = 'admins-list'),
    # endpoint where the user can see detail information
    # about your account
    path('client/me', UserOwnerProfile.as_view(),
      name="my-profile"),
    # endpoint where the user can see detail information
    # about any user profile
    path('client/profile/<int:pk>', UserProfile.as_view(),
      name="profile-detail"),
    #endpoint at which a password change request
    path('client/request-reset/password', RequestPasswordReset.as_view(),
      name="request-reset-password"),
    #endpoint where the password is reset according
    # to the data sent to the mail
    path('client/password/reset-complete', SetNewPassword.as_view(),
      name='password-reset-complete'),
     #endpoint for account verification by mail
    path('client/email/verify', EmailVerify.as_view(), name="email-verify"),
]
