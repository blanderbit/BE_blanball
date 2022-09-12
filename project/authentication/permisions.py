
from rest_framework import permissions

class IsNotAuthenticated(permissions.BasePermission):
    '''allows access only to admin users'''
    def has_permission(self, request, view):
        if request.user.id == None:
            return True
