from datetime import date
from types import NoneType

from .models import *
from .serializers import *
from .documents import *
from project.services import *
from .permisions import IsNotAuthenticated

from elasticsearch_dsl import Q

from rest_framework import generics,filters,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


def count_age(profile:Profile,data:dict) -> Profile:
    for item in data:
        if item[0] == 'birthday':
            birthday:date = item[1]
            age:int = (timezone.now().date() - birthday) // timezone.timedelta(days=365)
            profile.age:int = age
            return profile.save()

def send_email_template(user:User,body_title:str,title:str,text:str) -> None:
    context = ({'user_name': user.profile.name,'user_last_name':user.profile.last_name,
    'date_time':timezone.now(),'body_title':body_title,'title':title,'text':text})
    message:str = render_to_string('email_confirm.html',context)
    Util.send_email.delay(data = {'email_body':message,'to_email': 'shapranov.nik@gmail.com'})

class RegisterUser(generics.GenericAPIView):
    '''register user'''
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request) -> Response:
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        profile:Profile = Profile.objects.create(**serializer.validated_data['profile'])
        count_age(profile=profile,data = serializer.validated_data['profile'].items())
        serializer.save(profile = profile)
        send_email_template(user=User.objects.get(profile=profile.id),body_title=REGISTER_SUCCESS_BODY_TITLE,title=REGISTER_SUCCESS_TITLE,
        text=REGISTER_SUCCESS_TEXT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginUser(generics.GenericAPIView):
    '''user login'''
    serializer_class = LoginSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOwnerProfile(generics.GenericAPIView):
    '''get put delete private user profile'''
    serializer_class = UserSerializer
    
    def get(self,request) -> Response:
        user:User = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request) -> Response:
        code_create(email=request.user.email,type=ACCOUNT_DELETE_CODE_TYPE,
        dop_info = request.user.email)
        return Response(SENT_CODE_TO_EMAIL_SUCCESS,status=status.HTTP_200_OK)

class UpdateProfile(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = User.objects.all()

    def put(self, request) -> Response:
        user:User = self.queryset.get(id=self.request.user.id)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception = True)
        profile:Profile = Profile.objects.filter(id =user.profile_id)
        profile.update(**serializer.validated_data['profile'])
        count_age(profile=profile[0],data = serializer.validated_data['profile'].items())
        serializer.validated_data.pop('profile')
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserProfile(generics.GenericAPIView):
    '''get public user profile'''
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self,request,pk) -> Response:
        fields:list = ['configuration']
        try:
            user:User = self.queryset.get(id=pk)
            for item in user.configuration.items():
                if item[1] == True:
                    serializer = self.serializer_class(user,fields=(fields))
                elif item[1] == False:
                    fields.append(item[0])
                    serializer = self.serializer_class(user,fields=(fields))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_404_NOT_FOUND)

class UserList(generics.ListAPIView):
    '''get all users list'''
    serializer_class = UsersListSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter,)
    filterset_class = UserAgeRangeFilter
    search_fields = ('profile__name','profile__gender','profile__last_name')
    ordering_fields = ('id','profile__age','raiting')
    queryset = User.objects.filter(role='User').order_by('-id')

class AdminUsersList(UserList):
    '''displaying the full list of admin users'''
    def get_queryset(self) -> list:
        return self.queryset.filter(role = 'Admin')

class RequestPasswordReset(generics.GenericAPIView):
    '''send request to reset user password by email'''
    serializer_class = EmailSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request) -> Response:
        email:str = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            code_create(email=email,type=PASSWORD_RESET_CODE_TYPE,dop_info = None)
            return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)
        else:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_400_BAD_REQUEST)

class ResetPassword(generics.GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_code:str = serializer.validated_data['verify_code']
        try:
            code:Code = Code.objects.get(value=verify_code)
            user:User = User.objects.get(email=code.user_email)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            code.delete()
            send_email_template(user=user,body_title=REGISTER_SUCCESS_BODY_TITLE,title=REGISTER_SUCCESS_TITLE,
            text=REGISTER_SUCCESS_TEXT)
            return Response(PASSWORD_RESET_SUCCESS,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR,status=status.HTTP_404_NOT_FOUND) 

class RequestChangePassword(generics.GenericAPIView):
    serializer_class = RequestChangePasswordSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data.get('old_password')):
            return Response(WRONG_PASSWORD_ERROR, status=status.HTTP_400_BAD_REQUEST)
        code_create(email=request.user.email,type=PASSWORD_CHANGE_CODE_TYPE,
        dop_info = serializer.validated_data['new_password'])
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)

class RequetChangeEmail(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self,request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(email = serializer.validated_data['email']):
            code_create(email=request.user.email,type=EMAIL_CHANGE_CODE_TYPE,
            dop_info = serializer.validated_data['email'])
            return Response(SENT_CODE_TO_EMAIL_SUCCESS,status=status.HTTP_200_OK)
        return Response(THIS_EMAIL_ALREADY_IN_USE_ERROR,status=status.HTTP_400_BAD_REQUEST)

class RequestChangePhone(generics.GenericAPIView):
    serializer_class = RequestChangePhoneSerializer

    def post(self,request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code_create(email=request.user.email,type=PHONE_CHANGE_CODE_TYPE,
        dop_info = serializer.validated_data['phone'])
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=status.HTTP_200_OK)


class CheckCode(generics.GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = CheckCodeSerializer

    user:User =  None
    code:User =  None

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify_code:str = serializer.validated_data["verify_code"]
        self.code:Code = Code.objects.get(verify_code=verify_code)
        self.user:User = User.objects.get(id = request.user.id)
        if self.code.user_email != self.user.email:
            return Response(NO_PERMISSIONS_ERROR,status=status.HTTP_400_BAD_REQUEST)
        if self.code.type == PASSWORD_CHANGE_CODE_TYPE:
            self.user.set_password(self.code.dop_info)
            self.success(email_body='change password success')
            return Response(CHANGE_PASSWORD_SUCCESS,status=status.HTTP_200_OK) 
        elif self.code.type == EMAIL_CHANGE_CODE_TYPE:
            self.user.email = self.code.dop_info
            self.success(email_body='change email success')
            return Response(CHANGE_EMAIL_SUCCESS,status=status.HTTP_200_OK) 
        elif self.code.type == EMAIL_VERIFY_CODE_TYPE:
            self.user.is_verified = True
            self.success(email_body='email verify success')
            return Response(ACTIVATION_SUCCESS,status=status.HTTP_200_OK)
        elif self.code.type == PHONE_CHANGE_CODE_TYPE:
            self.user.phone = self.code.dop_info
            self.success(email_body='change phone success')
            return Response(CHANGE_PHONE_SUCCESS,status=status.HTTP_200_OK)
        elif self.code.type == ACCOUNT_DELETE_CODE_TYPE:
            User.objects.filter(id=self.user.id).delete()
            return Response(ACCOUNT_DELETED_SUCCESS,status=status.HTTP_200_OK)


    def success(self,) -> None:
        self.user.save()
        self.code.delete()
        send_email_template(user=self.user,body_title=REGISTER_SUCCESS_BODY_TITLE,title=REGISTER_SUCCESS_TITLE,
        text=REGISTER_SUCCESS_TEXT)

class RequestEmailVerify(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def get(self,request) -> Response:
        user:User = request.user
        if user.is_verified:
            return Response(ALREADY_VERIFIED_ERROR,status=status.HTTP_400_BAD_REQUEST)
        code_create(email=user.email,type=EMAIL_VERIFY_CODE_TYPE,
        dop_info = user.email)
        return Response(SENT_CODE_TO_EMAIL_SUCCESS,status=status.HTTP_200_OK)

class CheckUserActive(generics.GenericAPIView):
    serializer_class = CheckUserActiveSerializer

    def post(self,request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ActiveUser.objects.get(user_id = serializer.validated_data['user_id'])
            return Response({True:'User active'})
        except ActiveUser.DoesNotExist:
            return Response({False:'User not active'})


from .documents import ProfileDocument
from .serializers import ProductDocumentSerializer

class ProfileSearch(APIView):
    serializer_class = ProductDocumentSerializer
    document_class = ProfileDocument

    def generate_q_expression(self, query) -> dict:
        return Q("match", name={"query": query, "fuzziness": "auto"})

    def get(self, request, query):
        q = self.generate_q_expression(query)
        search = self.document_class.search().query(q)
        return Response(self.serializer_class(search.to_queryset(), many=True).data)