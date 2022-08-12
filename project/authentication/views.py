from .serializers import *
from .models import *
from .utils import *
from rest_framework import generics,filters,permissions,status,response,views
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse


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
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token  
        current_site = get_current_site(request).domain
        absurl = 'http://'+current_site+'?token='+str(token)
        email_body = f'Hi,{user.username}, use the link below to verify your email \n {absurl}'
        data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'}
        Util.send_email(data)
        return response.Response(user_data, status=status.HTTP_201_CREATED)



class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)



class UserOwnerProfile(views.APIView):
    def get(self,request):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserProfileSerializer(user)
        return response.Response (serializer.data)

    def put(self, request):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset  = User.objects.all()

class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email')
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = "User").id) 

class AdminUsersList(generics.ListAPIView):
    '''displaying the full list of admin users'''
    serializer_class = UserListSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('id','email')
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = "Admin").id)