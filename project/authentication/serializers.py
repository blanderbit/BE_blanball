from rest_framework import serializers,status
from .models import *
from project.constaints import *
from django.contrib import auth
from .validators import CodeValidator
import re

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



class EventUsersProfileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','last_name','avatar','position']

class EventAuthorSerializer(serializers.ModelSerializer):
    profile = EventUsersProfileSerializer(fields=('position',))
    class Meta:
        model = User
        fields = ['phone','profile']

class EventUsersSerializer(serializers.ModelSerializer):
    profile = EventUsersProfileSerializer()
    class Meta:
        model = User
        fields = ['profile']



class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Profile
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CreateUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Profile
        exclude = ('created_at','age')

class UpdateProfileSerializer(serializers.ModelSerializer):
    profile = CreateUpdateProfileSerializer()
    class Meta:
        model = User
        fields = ('configuration','profile','get_planned_events')

    def validate(self,attrs):
        conf =  attrs.get('configuration')
        keys = ['email','phone']
        planned_events =  attrs.get('get_planned_events')
        num = re.findall(r'\d{1,10}', planned_events)[0]
        str = re.findall(r'\D', planned_events)[0]
        if str not in ['d','m','y']:
            raise serializers.ValidationError(GET_PLANNED_IVENTS_ERROR,status.HTTP_400_BAD_REQUEST) 
        errors = []
    
        if not conf.keys():
            raise serializers.ValidationError(CONFIGURATION_IS_REQUIRED_ERROR,status.HTTP_400_BAD_REQUEST) 
        for key in conf.keys():
            if key not in keys:
                errors.append(key)  
        if errors:
            raise serializers.ValidationError(CANNOT_HIDE_SHOW_THIS_FIELD_ERROR.format(key=errors),status.HTTP_400_BAD_REQUEST) 
        return super().validate(attrs)

    def update(self, instance, validated_data):
        return super().update(instance,validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    '''a class that serializes user registration'''
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    re_password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    profile = CreateUpdateProfileSerializer()
    class Meta:
        model = User
        fields = ['email','phone','password','re_password','role','profile']

    def validate(self, attrs):
        '''data validation function'''
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
        # fields = ['id','phone','email','role','raiting','is_verified','profile','configuration','current_rooms']
        exclude = ('updated_at','raiting','password')


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3,max_length=255)

    class Meta:
        fields = ['email']
class RequestChangePhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model =  User
        fields = ['phone']

class RequestChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8, max_length=68)
    old_password = serializers.CharField(
        min_length=8, max_length=68)

    class Meta:
        fields = ['new_password','old_password']


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    verify_code = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        validators = [CodeValidator(token_type = PASSWORD_RESET_CODE_TYPE)]
        fields = ['verify_code','new_password']


class CheckCodeSerializer(serializers.Serializer):
    verify_code = serializers.CharField(
        min_length=5,max_length=5, write_only=True)

    class Meta:
        validators = [CodeValidator(token_type = [PASSWORD_CHANGE_CODE_TYPE,EMAIL_CHANGE_CODE_TYPE,
        EMAIL_VERIFY_CODE_TYPE,PHONE_CHANGE_CODE_TYPE])]
        fields = ['verify_code']

class AccountDeleteSerializer(serializers.ModelSerializer):
    '''class that serializes user verification by mail'''
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']

