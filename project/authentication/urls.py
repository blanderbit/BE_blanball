from authentication.views import (
    RegisterUser,
    LoginUser,
    UserList,
    UsersRelevantList,
    AdminUsersList,
    UserOwnerProfile,
    UserProfile,
    RequestPasswordReset,
    ResetPassword,
    RequestChangePassword,
    CheckCode,
    UpdateProfile,
    RequetChangeEmail,
    RequestChangePhone,
    CheckUserActive,
    RequestEmailVerify,
    GetImage,
)

from django.urls import path

urlpatterns = [
    # endpoint where user can register
    path('client/register', RegisterUser.as_view(), 
        name = 'register'),
    # endpoint where user can login
    path('client/login', LoginUser.as_view(), 
        name = 'login'),
    # endpoint where user can get users list
    path('client/users/list', UserList.as_view(), 
        name = 'users-list'),
    # endpoint where user can get relevant users list
    path('client/users/relevant/list', UsersRelevantList.as_view(),
        name = 'users-relevant-list'),
    # endpoint where user can get admins list
    path('admins/list', AdminUsersList.as_view(), 
        name = 'admins-list'),
    # endpoint where user can get his profile
    path('client/me', UserOwnerProfile.as_view(), 
        name = 'my-profile'),
    # endpoint where user can get profile of any user
    path('client/profile/<int:pk>', UserProfile.as_view(), 
        name = 'user-profile'),
    # endpoint where user can request reset password
    path('client/request-reset/password', RequestPasswordReset.as_view(), 
        name = 'request-reset-password'),
    # endpoint where user can confirm password reset
    path('client/password/reset-complete', ResetPassword.as_view(), 
        name = 'complete-reset-password'),
    # endpoint where user can request change password
    path('client/request-change/password', RequestChangePassword.as_view(), 
        name = 'request-change-password'),
    # endpoint where user can confirm password chagne,
    # email change,phone change,account verification
    path('client/check/code', CheckCode.as_view(), 
        name = 'check-code'),
    # endpoint where user can update his profile
    path('client/me/update', UpdateProfile.as_view(), 
        name = 'update-my-profile'),
    # endpoint where user can request change email
    path('client/request-change/email', RequetChangeEmail.as_view(), 
        name = 'request-change-email'),
    # endpoint where user can request change phone
    path('client/request-change/phone', RequestChangePhone.as_view(), 
        name = 'request-change-phone'),
    # endpoint where user can check is another user active
    path('client/search/user/active', CheckUserActive.as_view(),
        name = 'check-user-active'),
    # endpoint where user can check is another user active
    path('client/request-verify/email', RequestEmailVerify.as_view(), 
        name = 'request-email-verify'),
    path('client/get/image/<str:image_path>', GetImage.as_view(), 
        name = 'get-image'),
]