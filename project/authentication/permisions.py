from rest_framework import permissions
from authentication.models import Role

def CheckRole(role_id,role_names):
    if Role.objects.get(id = role_id).name in role_names:
        return True


class IsSuperOrDefaultAdmin(permissions.BasePermission):
    '''allows access only to admin users'''
    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user and CheckRole(role_id = request.user.role_id,role_names = ["User","Admin"]))
        else:
            return bool(request.user and CheckRole(role_id = request.user.role_id,role_names = ["Admin"]))



class IsNotAuthenticated(permissions.BasePermission):
    '''allows access only to admin users'''
    def has_permission(self, request, view):
        if request.user.id == None:
            return True
