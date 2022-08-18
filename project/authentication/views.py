from .serializers import *
from .models import *
from .tasks import Util
from rest_framework import generics,filters,permissions,status,response,views
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.sites.shortcuts import get_current_site
from project.services import code_create

class RegisterUser(generics.GenericAPIView):
    '''register user'''
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        profile = Profile.objects.create(**serializer.validated_data['profile'])
        serializer.save(profile = profile)
        user_data = serializer.data
        code_create(email=user_data['email'],k=3,type='email_verify')
        return response.Response(user_data, status=status.HTTP_201_CREATED)

class EmailVerify(generics.GenericAPIView):
    '''account verify by email'''
    serializer_class = EmailVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data["uidb64"]
        code = Code.objects.filter(value = uidb64)
        uidb64 = uidb64[:2]
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        user.is_verified = True
        user.save()
        code.delete()
        return response.Response(ACTIVATION_SUCCESS, status=status.HTTP_200_OK)


class LoginUser(generics.GenericAPIView):
    '''user login'''
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class UserOwnerProfile(generics.GenericAPIView):
    '''get put delete private user profile'''
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user = User.objects.get(id=self.request.user.id)
        serializer = self.serializer_class(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = User.objects.get(id=self.request.user.id)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        User.objects.get(id=self.request.user.id).delete()
        return response.Response(ACCOUNT_DELETED_SUCCESS,status=status.HTTP_200_OK)


class UserProfile(generics.RetrieveAPIView):
    '''get public user profile'''
    serializer_class = UserProfileSerializer
    queryset  = User.objects.all()

class UserList(generics.ListAPIView):
    '''get all users list'''
    serializer_class = UserListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email')
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = USER_ROLE).id) 

class AdminUsersList(generics.ListAPIView):
    '''displaying the full list of admin users'''
    serializer_class = UserListSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email')
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = ADMIN_ROLE).id)



class RequestPasswordReset(generics.GenericAPIView):
    '''send request to reset user password by email'''
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            code_create(email=email,k=3,type='password_reset')
            return response.Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)
        else:
            return response.Response(NO_SUCH_USER_ERROR, status=status.HTTP_200_OK)



class SetNewPassword(generics.GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = SetNewPasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data["uidb64"]
        code = Code.objects.filter(value = uidb64)
        uidb64 = uidb64[:2]
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        code.delete()
        return response.Response(PASSWORD_RESET_SUCCESS, status=status.HTTP_200_OK)

