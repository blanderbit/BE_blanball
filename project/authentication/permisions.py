from authentication.models import Role

from rest_framework import permissions

def CheckRole(role_id:int,role_names):
    if Role.objects.get(id = role_id).name in role_names:
        return True

class IsNotAuthenticated(permissions.BasePermission):
    '''allows access only to admin users'''
    def has_permission(self, request, view):
        if request.user.id == None:
            return True
