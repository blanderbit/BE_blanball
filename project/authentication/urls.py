from .views import *
from django.urls import path


urlpatterns = [
    # endpoint where the user can create an account
    path('client/register', RegisterUser.as_view(), 
      name="register"),
    # endpoint where the user can log into a previously created account
    path('client/login', LoginUser.as_view(), 
      name="login"),
    # endpoint where client can check all users list
    path('client/user/list',UserList.as_view(),
      name = 'user-list'),
    # endpoint where admin can check all admins list
    path('admin/list',AdminUsersList.as_view(),
        name = 'admin-list'),
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
    path('client/password/reset-complete', ResetPassword.as_view(),
      name='password-reset-complete'),
     #endpoint for account verification by mail
    path('client/email/verify', EmailVerify.as_view(), 
      name="email-verify"),
    #endpoint at which a password change request
    path('client/request-change/password', RequestChangePassword.as_view(),
      name="request-change-password"),
    #endpoint where the password is reset according
    # to the data sent to the mail
    path('client/password/change-complete', ChangePassword.as_view(),
      name='password-change-complete'),
    # endpoint where user can delete her account
    path('client/account/delete', AccountDelete.as_view(), 
      name="account-delete"),
]