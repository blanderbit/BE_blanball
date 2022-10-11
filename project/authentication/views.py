from typing import Any
from project.pagination import CustomPagination

from django.db.models.query import QuerySet

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.serializers import ValidationError

from authentication.models import (
    User,
    Profile,
    Code,
    ActiveUser,
)
from authentication.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UpdateProfileSerializer,
    UsersListSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    RequestChangePasswordSerializer,
    RequestChangePhoneSerializer,
    CheckCodeSerializer,
    CheckUserActiveSerializer,
)
from authentication.services import (
    count_age,
    send_email_template,
    code_create,
    profile_update,
    reset_password,
)
from authentication.permisions import IsNotAuthenticated
from authentication.filters import (
    RankedFuzzySearchFilter,
    UserAgeRangeFilter,
)

from authentication.constaints import (
    REGISTER_SUCCESS_BODY_TITLE, REGISTER_SUCCESS_TITLE, REGISTER_SUCCESS_TEXT, SENT_CODE_TO_EMAIL_SUCCESS, ACCOUNT_DELETE_CODE_TYPE,
    PASSWORD_RESET_CODE_TYPE, NO_SUCH_USER_ERROR, PASSWORD_CHANGE_CODE_TYPE, WRONG_PASSWORD_ERROR, PASSWORD_RESET_SUCCESS,
    EMAIL_VERIFY_CODE_TYPE, ALREADY_VERIFIED_ERROR, PHONE_CHANGE_CODE_TYPE, EMAIL_CHANGE_CODE_TYPE, THIS_EMAIL_ALREADY_IN_USE_ERROR,
    TEMPLATE_SUCCESS_BODY_TITLE, TEMPLATE_SUCCESS_BODY_TITLE, NO_PERMISSIONS_ERROR, TEMPLATE_SUCCESS_TITLE, TEMPLATE_SUCCESS_TEXT,
    ACTIVATION_SUCCESS, CHANGE_PHONE_SUCCESS, CHANGE_PASSWORD_SUCCESS,EMAIL_VERIFY_SUCCESS_BODY_TITLE, EMAIL_VERIFY_SUCCESS_TITLE,
    CHANGE_EMAIL_SUCCESS, ACCOUNT_DELETED_SUCCESS, EMAIL_VERIFY_SUCCESS_TEXT, ACCOUNT_DELETE_SUCCESS_TEXT, 
    ACCOUNT_DELETE_SUCCESS_BODY_TITLE, ACCOUNT_DELETE_SUCCESS_TITLE,
)


class RegisterUser(GenericAPIView):
    '''register user'''
    serializer_class = RegisterSerializer
    permission_classes = (IsNotAuthenticated, )

    def post(self, request: Request) -> Response:
        user: dict[str, Any] = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        profile: Profile = Profile.objects.create(**serializer.validated_data['profile'])
        count_age(profile = profile, data = serializer.validated_data['profile'].items())
        serializer.save(profile = profile)
        send_email_template(user = User.objects.get(profile = profile.id), 
        body_title = REGISTER_SUCCESS_BODY_TITLE, title = REGISTER_SUCCESS_TITLE,
        text = REGISTER_SUCCESS_TEXT)
        return Response(serializer.data, status = HTTP_201_CREATED)

class LoginUser(GenericAPIView):
    '''user login'''
    serializer_class = LoginSerializer
    permission_classes = (IsNotAuthenticated, )

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = HTTP_200_OK)

class UserOwnerProfile(GenericAPIView):
    serializer_class = UserSerializer
    
    def get(self, request: Request) -> Response: 
        '''get detailed information about your profile'''
        user: User = User.objects.get(id = self.request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status = HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        '''submitting an account deletion request'''
        code_create(email = request.user.email, type = ACCOUNT_DELETE_CODE_TYPE,
        dop_info = request.user.email)
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status=HTTP_200_OK)

class UpdateProfile(GenericAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = User.objects.all()

    def put(self, request: Request) -> Response: 
        '''changing profile information'''
        user: User = self.queryset.get(id = self.request.user.id)
        serializer = self.serializer_class(user, data = request.data)
        profile_update(user = user, serializer = serializer)
        return Response(serializer.data, status = HTTP_200_OK)


class UserProfile(GenericAPIView):
    '''get public user profile'''
    serializer_class = UserSerializer
    queryset: QuerySet[User] = User.objects.all()

    def get(self, request: Request, pk: int) -> Response:
        '''getting a public user profile'''
        fields: list = ['configuration']
        try:
            user: User = self.queryset.get(id = pk)
            for item in user.configuration.items():
                if item[1] == True:
                    serializer = self.serializer_class(user, fields = (fields))
                elif item[1] == False:
                    fields.append(item[0])
                    serializer = self.serializer_class(user, fields = (fields))
            return Response(serializer.data, status = HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR, status = HTTP_404_NOT_FOUND)


class UserList(ListAPIView):
    '''get all users list'''
    serializer_class = UsersListSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter, )
    filterset_class = UserAgeRangeFilter
    search_fields = ('profile__name', 'profile__gender', 'profile__last_name')
    ordering_fields = ('id', 'profile__age', 'raiting')
    queryset = User.objects.filter(role = 'User').select_related('profile').order_by('-id')

class UsersRelevantList(ListAPIView):
    '''getting the 5 most relevant users for your query'''
    filter_backends = (RankedFuzzySearchFilter, )
    serializer_class = UsersListSerializer
    queryset = User.objects.filter(role = 'User').select_related('profile')
    search_fields = ('profile__name', 'profile__last_name')

class AdminUsersList(UserList):
    '''displaying the full list of admin users'''
    def get_queryset(self) -> QuerySet[User]:
        return self.queryset.filter(role = 'Admin')

class RequestPasswordReset(GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = (IsNotAuthenticated, )

    def post(self, request: Request) -> Response:
        '''send request to reset user password by email'''
        email: str = request.data.get('email', '')
        if User.objects.filter(email = email).exists():
            code_create(email = email, type = PASSWORD_RESET_CODE_TYPE, dop_info = None)
            return Response(SENT_CODE_TO_EMAIL_SUCCESS, status = HTTP_200_OK)
        else:
            return Response(NO_SUCH_USER_ERROR, status = HTTP_400_BAD_REQUEST)

class ResetPassword(GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = ResetPasswordSerializer
    permission_classes = (IsNotAuthenticated, )

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            reset_password(serializer = serializer)
            return Response(PASSWORD_RESET_SUCCESS, status = HTTP_200_OK)
        except User.DoesNotExist:
            return Response(NO_SUCH_USER_ERROR, status = HTTP_404_NOT_FOUND) 

class RequestChangePassword(GenericAPIView):
    serializer_class = RequestChangePasswordSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        if not request.user.check_password(serializer.data.get('old_password')):
            return Response(WRONG_PASSWORD_ERROR, status = HTTP_400_BAD_REQUEST)
        code_create(email=request.user.email,type = PASSWORD_CHANGE_CODE_TYPE,
        dop_info = serializer.validated_data['new_password'])
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status = HTTP_200_OK)

class RequestEmailVerify(GenericAPIView):
    serializer_class = EmailSerializer

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_verified:
            return Response(ALREADY_VERIFIED_ERROR, status = HTTP_400_BAD_REQUEST)
        code_create(email = user.email, type = EMAIL_VERIFY_CODE_TYPE,
        dop_info = user.email)
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status = HTTP_200_OK)

class CheckUserActive(GenericAPIView):
    serializer_class = CheckUserActiveSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            ActiveUser.objects.get(user_id = serializer.validated_data['user_id'])
            return Response({True: 'User active'})
        except ActiveUser.DoesNotExist:
            return Response({False: 'User not active'})

class RequetChangeEmail(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        if not User.objects.filter(email = serializer.validated_data['email']):
            code_create(email = request.user.email, type = EMAIL_CHANGE_CODE_TYPE,
            dop_info = serializer.validated_data['email'])
            return Response(SENT_CODE_TO_EMAIL_SUCCESS, status = HTTP_200_OK)
        return Response(THIS_EMAIL_ALREADY_IN_USE_ERROR, status = HTTP_400_BAD_REQUEST)

class RequestChangePhone(GenericAPIView):
    serializer_class = RequestChangePhoneSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        code_create(email = request.user.email,type = PHONE_CHANGE_CODE_TYPE,
        dop_info = serializer.validated_data['phone'])
        return Response(SENT_CODE_TO_EMAIL_SUCCESS, status = HTTP_200_OK)

class CheckCode(GenericAPIView):
    '''password reset on a previously sent request'''
    serializer_class = CheckCodeSerializer

    def success(self, key: str) -> None:
        self.user.save()
        self.code.delete()
        send_email_template(user = self.user, body_title = TEMPLATE_SUCCESS_BODY_TITLE.format(key = key),
        title = TEMPLATE_SUCCESS_TITLE.format(key = key),
        text = TEMPLATE_SUCCESS_TEXT.format(key = key))

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        verify_code: str = serializer.validated_data['verify_code']
        self.code: Code = Code.objects.get(verify_code = verify_code)
        self.user: User = User.objects.get(id = request.user.id)
        if self.code.user_email != self.user.email:
            raise ValidationError(NO_PERMISSIONS_ERROR, HTTP_400_BAD_REQUEST)

        if self.code.type == PASSWORD_CHANGE_CODE_TYPE:
            self.user.set_password(self.code.dop_info)
            self.success(key = 'password')
            return Response(CHANGE_PASSWORD_SUCCESS, status = HTTP_200_OK) 
 
        elif self.code.type == PHONE_CHANGE_CODE_TYPE:
            self.user.phone = self.code.dop_info
            self.success(key = 'phone number')
            return Response(CHANGE_PHONE_SUCCESS, status = HTTP_200_OK)
            
        elif self.code.type == EMAIL_CHANGE_CODE_TYPE:
            self.user.email = self.code.dop_info
            self.success(key = 'email')
            return Response(CHANGE_EMAIL_SUCCESS, status = HTTP_200_OK) 

        elif self.code.type == ACCOUNT_DELETE_CODE_TYPE:
            send_email_template(user = self.user, body_title = ACCOUNT_DELETE_SUCCESS_BODY_TITLE, title = ACCOUNT_DELETE_SUCCESS_TITLE,
            text = ACCOUNT_DELETE_SUCCESS_TEXT)
            User.objects.filter(id = self.user.id).delete()
            self.code.delete()
            return Response(ACCOUNT_DELETED_SUCCESS, status = HTTP_200_OK)

        elif self.code.type == EMAIL_VERIFY_CODE_TYPE:
            self.user.is_verified = True
            self.user.save()
            self.code.delete()
            send_email_template(user = self.user, body_title = EMAIL_VERIFY_SUCCESS_BODY_TITLE, title = EMAIL_VERIFY_SUCCESS_TITLE,
            text = EMAIL_VERIFY_SUCCESS_TEXT)
            return Response(ACTIVATION_SUCCESS, status = HTTP_200_OK)
