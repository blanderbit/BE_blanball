from rest_framework import serializers
from .models import *
from project.constaints import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    '''a class that serializes user registration'''
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    re_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'username', 'password','re_password','profile']

    def validate(self, attrs):
        '''data validation function'''
        email = attrs.get('email', ''),
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        re_password = attrs.get('re_password', '')

        if password != re_password :
            raise serializers.ValidationError(PASSWORD_DO_NOT_MATCH) 

        if not username.isalnum():
            raise serializers.ValidationError(
                DEFAULT_SERIALIZER_ERROR)
        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password")
        '''creating a user with previously validated data'''
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    '''class that serializes user login'''
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        '''function that issues jwt tokens for an authorized user'''
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        '''data validation function for user authorization'''
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(INVALID_CREDENTIALS_ERROR)
        if not user.is_verified:
            raise AuthenticationFailed(NOT_VERIFIED_BY_EMAIL_ERROR)

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['username','email','role','profile']
        

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','last_login','updated_at']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'