import jwt
import abc

from .models import *
from .serializers import *
from .documents import *
from project.services import *
from notifications.models import Notification
from .permisions import IsNotAuthenticated
from events.models import Event

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings


from elasticsearch_dsl import Q

from rest_framework import generics,filters,permissions,status,response,views
from django_filters.rest_framework import DjangoFilterBackend



def user_delete(pk):
    Code.objects.filter(user_email = User.objects.get(id = pk).email).delete()
    Event.objects.filter(author_id = pk).delete()
    Notification.objects.filter(user_id = pk).delete()
    Profile.objects.filter(id = pk).delete()
    User.objects.filter(id = pk).delete()

def count_age(profile,data):
    for item in data:
        if item[0] == 'birthday':
            birthday = item[1]
            age = (timezone.now().date() - birthday) // timezone.timedelta(days=365)
            profile.age = age
            return profile.save()

class RegisterUser(generics.GenericAPIView):
    '''register user'''
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        profile = Profile.objects.create(**serializer.validated_data['profile'])
        count_age(profile=profile,data = serializer.validated_data['profile'].items())
        serializer.save(profile = profile)
        context = ({'name':profile.name,'surname':profile.last_name})
        message = render_to_string('email_message',context)
        Util.send_email.delay(data = {'email_subject': 'Регистарция','email_body':message,'to_email': user['email']})
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginUser(generics.GenericAPIView):
    '''user login'''
    serializer_class = LoginSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    

class AccountDelete(generics.GenericAPIView):
    serializer_class = AccountDeleteSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            Util.send_email.delay(data = {'email_subject': 'Удалание аккаунта','email_body': f'{user.profile.name},аккаунт удален!' ,'to_email': user['email']})
            user_delete(pk = user.id)
            return  response.Response(ACCOUNT_DELETED_SUCCESS,status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return response.Response(CODE_EXPIRED_ERROR,status=status.HTTP_400_BAD_REQUEST)
        except:
            return response.Response(BAD_CODE_ERROR,status=status.HTTP_400_BAD_REQUEST)   


class UserOwnerProfile(generics.GenericAPIView):
    '''get put delete private user profile'''
    pagination_class = None
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request):
        token = RefreshToken.for_user(request.user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('account-delete')
        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body = f'Hi,{request.user.profile.name}, use the link below to delete your account \n {absurl}'
        Util.send_email.delay(data = {'email_body': email_body, 'to_email': request.user.email,
        'email_subject': 'Verify your email'})
        return response.Response(SENT_CODE_TO_EMAIL_SUCCESS , status=status.HTTP_200_OK)

class UpdateProfile(generics.GenericAPIView):
    pagination_class = None
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def put(self, request):
        user = self.queryset.get(id=self.request.user.id)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception = True)
        profile = Profile.objects.filter(id =user.profile_id)
        profile.update(**serializer.validated_data['profile'])
        count_age(profile=profile[0],data = serializer.validated_data['profile'].items())
        serializer.validated_data.pop('profile')
        serializer.save()
        return response.Response(serializer.data,status=status.HTTP_200_OK)


class UserProfile(generics.GenericAPIView):
    '''get public user profile'''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset  = User.objects.all()

    def get(self,request,pk):
        fields = ['configuration']
        try:
            user = self.queryset.get(id=pk)
            for item in user.configuration.items():
                if item[1] == True:
                    serializer = self.serializer_class(user,fields=(fields))
                elif item[1] == False:
                    fields.append(item[0])
                    serializer = self.serializer_class(user,fields=(fields))
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return response.Response(NO_SUCH_USER_ERROR,status=status.HTTP_404_NOT_FOUND)

class UserList(generics.ListAPIView):
    '''get all users list'''
    serializer_class = ProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('name','age','gender','last_name')
    queryset = Profile.objects.all()


class AdminUsersList(generics.ListAPIView):
    '''displaying the full list of admin users'''
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email','phone')
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
            code_create(email=email,k=5,type=PASSWORD_RESET_CODE_TYPE,dop_info = None)
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
        Util.send_email.delay(data = {'email_subject': 'Reset password','email_body': f'{user.profile.name}, reset password success!' ,'to_email': user.email})
        return response.Response(PASSWORD_RESET_SUCCESS, status=status.HTTP_200_OK) 



class RequestChangePassword(generics.GenericAPIView):
    serializer_class = RequestChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data.get("old_password")):
            return response.Response(WRONG_PASSWORD_ERROR, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_create(email=request.user.email,k=5,type=PASSWORD_CHANGE_CODE_TYPE,
            dop_info =  serializer.validated_data['new_password'])
            return response.Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)

class RequetChangeEmail(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordRequestSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(email = serializer.validated_data['email']):
            code_create(email=request.user.email,k=5,type=EMAIL_CHANGE_CODE_TYPE,
            dop_info = serializer.validated_data['email'])
            return response.Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)
        return response.Response(THIS_EMAIL_ALREADY_IN_USE_ERROR, status=status.HTTP_400_BAD_REQUEST)

class RequestChangePhone(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestChangePhoneSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_create(email=request.user.email,k=5,type=PHONE_CHANGE_CODE_TYPE,
        dop_info =  serializer.validated_data['phone'])
        return response.Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)


class CheckCode(generics.GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = CheckCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    user =  None
    code =  None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_code = serializer.validated_data["verify_code"]
        self.code = Code.objects.get(value=verify_code)
        self.user = User.objects.get(id = request.user.id)
        if self.code.user_email != self.user.email:
            return response.Response(PASSWORD_CHANGE_ERROR,status=status.HTTP_400_BAD_REQUEST)
        if self.code.type == PASSWORD_CHANGE_CODE_TYPE:
            self.user.set_password(self.code.dop_info)
            self.success(email_subject='change password',email_body='change password success')
            return response.Response(CHANGE_PASSWORD_SUCCESS,status=status.HTTP_200_OK) 
        elif self.code.type == EMAIL_CHANGE_CODE_TYPE:
            self.user.email = self.code.dop_info
            self.success(email_subject='change email',email_body='change email success')
            return response.Response(CHANGE_EMAIL_SUCCESS,status=status.HTTP_200_OK) 
        elif self.code.type == EMAIL_VERIFY_CODE_TYPE:
            self.user.is_verified = True
            self.success(email_subject='email verify',email_body='email verify success')
            return response.Response(ACTIVATION_SUCCESS,status=status.HTTP_200_OK)
        elif self.code.type == PHONE_CHANGE_CODE_TYPE:
            self.user.phone = self.code.dop_info
            self.success(email_subject='change phone',email_body='change phone success')
            return response.Response(CHANGE_PHONE_SUCCESS,status=status.HTTP_200_OK)


    def success(self,email_subject,email_body):
        self.user.save()
        self.code.delete()
        data = {'email_subject': email_subject,'email_body': f'{self.user.profile.name}{email_body}!' ,'to_email': self.user.email}
        Util.send_email.delay(data)




class PaginatedElasticSearchAPIView(views.APIView,CustomPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return response.Response(e, status=500)

class SearchUsers(PaginatedElasticSearchAPIView):
    serializer_class = ProfileListSerializer
    document_class = ProfileDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'name',
                    'last_name',
                ], fuzziness='auto')