from .views import *

from django.urls import path


urlpatterns = [
    # endpoint where the user can create an account
    path('client/register', RegisterUser.as_view(),name='register'),
    # endpoint where the user can log into a previously created account
    path('client/login', LoginUser.as_view(),name='login'),
    # endpoint where client can check all users list
    path('client/users/list',UserList.as_view(),name='users-list'),
    # endpoint where admin can check all admins list
    path('admins/list',AdminUsersList.as_view(),name='admins-list'),
    # endpoint where the user can see detail information
    # about your account
    path('client/me', UserOwnerProfile.as_view(),name='my-profile'),
    # endpoint where the user can see detail information
    # about any user profile
    path('client/profile/<int:pk>', UserProfile.as_view(),name='user-profile'),
    #endpoint at which a password change request
    path('client/request-reset/password', RequestPasswordReset.as_view(),name='request-reset-password'),
    #endpoint where the password is reset according
    # to the data sent to the mail
    path('client/password/reset-complete', ResetPassword.as_view(),name='complete-reset-password'),
    #endpoint at which a password change request
    path('client/request-change/password', RequestChangePassword.as_view(),name='request-change-password'),

    path('client/check/code',CheckCode.as_view(),name='check-code'),
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
