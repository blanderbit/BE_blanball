import re

from collections import OrderedDict
from typing import Union

from django.contrib import auth

from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from authentication.models import (
    User,
    Profile,
)
from project.constaints import *
from authentication.validators import CodeValidator

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs) -> None:
        fields: tuple[str] = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are specified in the `fields` argument.
            existing = set(fields)
            for field_name in existing:
                self.fields.pop(field_name)

class EventUsersProfileSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'name',
            'last_name',
            'avatar',
            'position',
        )

class EventUsersSerializer(serializers.ModelSerializer):
    profile = EventUsersProfileSerializer()

    class Meta:
        model = User
        fields = ('profile',)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class CreateUpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Profile
        exclude = (
            'created_at',
            'age',
        )

class UpdateProfileSerializer(serializers.ModelSerializer):
    profile = CreateUpdateProfileSerializer()

    class Meta:
        model = User
        fields = (
            'configuration',
            'profile',
            'get_planned_events',
        )

    def validate(self,attrs:OrderedDict) -> Union[serializers.ValidationError,OrderedDict]:
        conf: str =  attrs.get('configuration')
        keys: tuple[str] = ('email','phone','send_email',)
        planned_events =  attrs.get('get_planned_events')
        string = re.findall(r'\D', planned_events)[0]
        if string not in ['d','m','y']:
            raise serializers.ValidationError(GET_PLANNED_IVENTS_ERROR,HTTP_400_BAD_REQUEST) 

        if sorted(conf) != sorted(keys):
            raise serializers.ValidationError(CONFIGURATION_IS_REQUIRED_ERROR,HTTP_400_BAD_REQUEST)

        return super().validate(attrs)

    def update(self, instance, validated_data) -> OrderedDict:
        return super().update(instance,validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    '''a class that serializes user registration'''
    password:str = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    re_password:str = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    profile:Profile = CreateUpdateProfileSerializer()

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'password',
            're_password',
            'profile',
        )

    def validate(self, attrs:OrderedDict) -> Union[serializers.ValidationError,OrderedDict]:
        '''data validation function'''
        password:str = attrs.get('password', '')
        re_password:str = attrs.get('re_password', '')
        
        if password != re_password :
            raise serializers.ValidationError(PASSWORDS_DO_NOT_MATCH,HTTP_400_BAD_REQUEST) 
        return attrs

    def create(self, validated_data: dict[str,any]) -> User:
        validated_data.pop("re_password")
        '''creating a user with previously validated data'''
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    '''class that serializes user login'''
    email:str = serializers.EmailField(min_length=3,max_length=255)
    password:str = serializers.CharField(min_length=8,
        max_length=68, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj) -> dict:
        '''function that issues jwt tokens for an authorized user'''
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = (
            'email', 
            'password', 
            'tokens',
        )

    def validate(self, attrs: OrderedDict) -> Union[serializers.ValidationError,dict[str,str],OrderedDict]:
        '''data validation function for user authorization'''
        email: str = attrs.get('email', '')
        password: str = attrs.get('password', '')
        user: User = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR,HTTP_400_BAD_REQUEST)
        return {
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class UserSerializer(DynamicFieldsModelSerializer):
    '''user pricate and public profile serializer'''
    profile:Profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'email',
            'role',
            'phone',
            'is_verified',
            'raiting',
            'profile',
            'configuration'
        )

class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Profile
        fields = (
            'id',
            'name',
            'last_name',
            'avatar',
            'position',
            'gender',
            'age',
        )

class UsersListSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer()

    class Meta:
        model =  User
        fields= (
            'profile',
            'raiting',
            'role',
        )


class EmailSerializer(serializers.Serializer):
    email: str = serializers.EmailField(min_length=3,max_length=255)

    class Meta:
        fields = ('email',)

        
class RequestChangePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('phone',)

class RequestChangePasswordSerializer(serializers.Serializer):
    new_password:str = serializers.CharField(
        min_length=8, max_length=68)
    old_password:str = serializers.CharField(
        min_length=8, max_length=68)

    class Meta:
        fields = (
            'new_password',
            'old_password',
        )


class ResetPasswordSerializer(serializers.Serializer):
    new_password:str = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    verify_code:str = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        validators = [CodeValidator(token_type = PASSWORD_RESET_CODE_TYPE)]
        fields = (
            'verify_code',
            'new_password',
        )


class CheckCodeSerializer(serializers.Serializer):
    verify_code:str = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        validators = [CodeValidator(token_type = [PASSWORD_CHANGE_CODE_TYPE,EMAIL_CHANGE_CODE_TYPE,
        EMAIL_VERIFY_CODE_TYPE,PHONE_CHANGE_CODE_TYPE,ACCOUNT_DELETE_CODE_TYPE])]
        fields = ('verify_code',)


class CheckUserActiveSerializer(serializers.Serializer):
    user_id: int = serializers.IntegerField(min_value=0)

    class Meta:
        fields = ('user_id',)

    def validate(self,attrs: OrderedDict) -> Union[OrderedDict,serializers.ValidationError]:
        user_id:int = attrs.get('user_id')
        try:
            User.objects.get(id = user_id)
            return super().validate(attrs)
        except User.DoesNotExist:
            raise serializers.ValidationError(NO_SUCH_USER_ERROR,HTTP_400_BAD_REQUEST)
