from .views import *

from django.urls import path


urlpatterns = [
    # endpoint where the user can create an account
    path('client/register', RegisterUser.as_view()),
    # endpoint where the user can log into a previously created account
    path('client/login', LoginUser.as_view()),
    # endpoint where client can check all users list
    path('client/user/list',UserList.as_view()),
    # endpoint where admin can check all admins list
    path('admin/list',AdminUsersList.as_view()),
    # endpoint where the user can see detail information
    # about your account
    path('client/me', UserOwnerProfile.as_view()),
    # endpoint where the user can see detail information
    # about any user profile
    path('client/profile/<int:pk>', UserProfile.as_view()),
    #endpoint at which a password change request
    path('client/request-reset/password', RequestPasswordReset.as_view()),
    #endpoint where the password is reset according
    # to the data sent to the mail
    path('client/password/reset-complete', ResetPassword.as_view()),
    #endpoint at which a password change request
    path('client/request-change/password', RequestChangePassword.as_view()),

    path('client/check/code',CheckCode.as_view()),
    #endpoint where user can delete her account
    path('client/me/delete', AccountDelete.as_view()),
    # endpoint where the user can see detail information
    # about your account
    path('client/me/update', UpdateProfile.as_view()),
    #endpoint at which a email change request
    path('client/request-change/email',RequetChangeEmail.as_view()),
    #endpoint at which a phone change request
    path('client/request-change/phone',RequestChangePhone.as_view()),

    path('client/search/user/<str:query>/',SearchUsers.as_view()),
]
