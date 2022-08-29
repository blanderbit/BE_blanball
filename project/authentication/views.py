from urllib import request
from notifications.models import Notification
from .serializers import *
from .models import *
from rest_framework import generics,filters,permissions,status,response,views
from django_filters.rest_framework import DjangoFilterBackend
from project.services import *
from events.models import Event
from .permisions import IsNotAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.shortcuts import redirect


def user_delete(pk):
    Code.objects.filter(user_email = User.objects.get(id = pk).email).delete()
    Event.objects.filter(author_id = pk).delete()
    Notification.objects.filter(user_id = pk).delete()
    Profile.objects.filter(id = pk).delete()
    User.objects.filter(id = pk).delete()

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
        code_create(email=user_data['email'],k=5,type=EMAIL_VERIFY_TOKEN_TYPE,dop_info = None)
        return response.Response(user_data, status=status.HTTP_201_CREATED)

class EmailVerify(generics.GenericAPIView):
    '''account verify by email'''
    serializer_class = EmailVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_code = serializer.validated_data["verify_code"]
        code = Code.objects.get(value=verify_code)
        user = User.objects.get(email=code.user_email)
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

    

class AccountDelete(views.APIView):
    serializer_class = AccountDeleteSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user_delete(pk = User.objects.get(id=payload['user_id']).id)
            return redirect("login")
        except jwt.ExpiredSignatureError:
            return response.Response("", status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return response.Response("", status=status.HTTP_400_BAD_REQUEST)



class UserOwnerProfile(generics.GenericAPIView):
    '''get put delete private user profile'''
    pagination_class = None
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user = User.objects.get(id=self.request.user.id)
        self.serializer_class =  UserSerializer
        serializer = UserSerializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = Profile.objects.get(id=self.request.user.profile_id)
        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        token = RefreshToken.for_user(request.user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('account-delete')
        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body = f'Hi,{request.user.profile.name}, use the link below to delete your account \n {absurl}'
        data = {'email_body': email_body, 'to_email': request.user.email,
            'email_subject': 'Verify your email'}
        Util.send_email.delay(data)
        return response.Response(SENT_CODE_TO_EMAIL_SUCCESS , status=status.HTTP_200_OK)


class UserProfile(generics.RetrieveAPIView):
    '''get public user profile'''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset  = User.objects.all()

class UserList(generics.ListAPIView):
    '''get all users list'''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email','phone')
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = USER_ROLE).id) 

class AdminUsersList(generics.ListAPIView):
    '''displaying the full list of admin users'''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email','phone','name')
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = ADMIN_ROLE).id)



class RequestPasswordReset(generics.GenericAPIView):
    '''send request to reset user password by email'''
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            code_create(email=email,k=5,type=PASSWORD_RESET_TOKEN_TYPE,dop_info = None)
            return response.Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)
        else:
            return response.Response(NO_SUCH_USER_ERROR,status=status.HTTP_400_BAD_REQUEST)



class ResetPassword(generics.GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_code = serializer.validated_data["verify_code"]
        code = Code.objects.get(value=verify_code)
        user = User.objects.get(email=code.user_email)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        code.delete()
        return response.Response(PASSWORD_RESET_SUCCESS, status=status.HTTP_200_OK) 



class RequestChangePassword(generics.GenericAPIView):
    serializer_class = RequestChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            if not request.user.check_password(serializer.data.get("old_password")):
                return response.Response(WRONG_PASSWORD_ERROR, status=status.HTTP_400_BAD_REQUEST)
            else:
                code_create(email=request.user.email,k=5,type=PASSWORD_CHANGE_TOKEN_TYPE,
                dop_info =  serializer.validated_data['new_password'])
                return response.Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)



class ChangePassword(generics.GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = Code.objects.get(value=verify_code)
        user = User.objects.get(id = request.user.id)
        if code.email != user.email:
            return response.Response(PASSWORD_CHANGE_ERROR, status=status.HTTP_400_BAD_REQUEST) 
        verify_code = serializer.validated_data["verify_code"]
        user.set_password(code.dop_info)
        user.save()
        code.delete()
        return response.Response(PASSWORD_CHANGE_SUCCESS, status=status.HTTP_200_OK) 

