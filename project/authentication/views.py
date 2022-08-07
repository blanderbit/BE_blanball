from .serializers import *
from .models import *
from rest_framework import generics,filters,permissions
from django_filters.rest_framework import DjangoFilterBackend

class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = '__all__'
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = "User").id) 

class AdminUsersList(generics.ListAPIView):
    '''displaying the full list of admin users'''
    serializer_class = UserListSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = '__all__'
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(role_id = Role.objects.get(name = "Admin").id)


class CreateRole(generics.CreateAPIView):
    serializer_class = RoleSerializer
    permission_classes = []
    queryset = Role.objects.all()