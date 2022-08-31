from rest_framework import serializers,status
from .models import *
from project.constaints import *
from django.contrib import auth
from django.utils import timezone


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are specified in the `fields` argument.
            existing = set(fields)
            for field_name in existing:
                self.fields.pop(field_name)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('configuration','profile')
    
    def validate(self,attrs):
        config =  attrs.get('configuration')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        return super().update(instance,validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    '''a class that serializes user registration'''
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    re_password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['email','phone','password','re_password','role','profile']

    def validate(self, attrs):
        '''data validation function'''
        email = attrs.get('email', ''),
        password = attrs.get('password', '')
        re_password = attrs.get('re_password', '')

        if password != re_password :
            raise serializers.ValidationError(PASSWORDS_DO_NOT_MATCH,status.HTTP_400_BAD_REQUEST) 

        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password")
        '''creating a user with previously validated data'''
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    '''class that serializes user login'''
    email = serializers.EmailField(min_length=3,max_length=255)
    password = serializers.CharField(min_length=8,
        max_length=68, write_only=True)

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
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        '''data validation function for user authorization'''
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR,status.HTTP_400_BAD_REQUEST)
        return {
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class UserSerializer(DynamicFieldsModelSerializer):
    '''user pricate and public profile serializer'''
    profile = ProfileSerializer()
    role = serializers.SlugRelatedField(
        slug_field="name", read_only = True)
    class Meta:
        model = User
        fields = ['id','phone','email','role','raiting','profile','configuration']


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3,max_length=255)

    class Meta:
        fields = ['email']



class RequestChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8, max_length=68)
    old_password = serializers.CharField(
        min_length=8, max_length=68)

    class Meta:
        fields = ['new_password','old_password']


class MultipleOf:
    def __init__(self, verify_code,code):
        self.verify_code = verify_code
        self.code = code

    def __call__(self, value):
        if not self.code:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = self.verify_code).type != PASSWORD_RESET_TOKEN_TYPE:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = self.verify_code).life_time < timezone.now():
            raise serializers.ValidationError(CODE_EXPIRED_ERROR,status.HTTP_400_BAD_REQUEST)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    verify_code = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        fields = ['verify_code','new_password']

    def validate(self, attrs):
        verify_code = attrs.get('verify_code')
        code = Code.objects.filter(value = verify_code)
        # validators = [MultipleOf(verify_code = attrs.get('verify_code'),code = Code.objects.filter(value = attrs.get('verify_code')))]
        if not code:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = verify_code).type != PASSWORD_RESET_TOKEN_TYPE:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = verify_code).life_time < timezone.now():
            raise serializers.ValidationError(CODE_EXPIRED_ERROR,status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)


class EmailVerifySerializer(serializers.Serializer):
    verify_code = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        fields = ['verify_code']
    
    def validate(self, attrs):
        verify_code = attrs.get('verify_code')
        code = Code.objects.filter(value = verify_code)
        if not code:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = verify_code).type != EMAIL_VERIFY_TOKEN_TYPE:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = verify_code).life_time < timezone.now():
            raise serializers.ValidationError(CODE_EXPIRED_ERROR,status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    verify_code = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        fields = ['verify_code']

    def validate(self, attrs):
        verify_code = attrs.get('verify_code')
        code = Code.objects.filter(value = verify_code)
        if not code:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = verify_code).type != PASSWORD_CHANGE_TOKEN_TYPE:
            raise serializers.ValidationError(BAD_CODE_ERROR,status.HTTP_400_BAD_REQUEST)
        elif Code.objects.get(value = verify_code).life_time < timezone.now():
            raise serializers.ValidationError(CODE_EXPIRED_ERROR,status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)



class AccountDeleteSerializer(serializers.ModelSerializer):
    '''class that serializes user verification by mail'''
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']


