from rest_framework import permissions
from rest_framework.request import Request


class IsNotAuthenticated(permissions.BasePermission):
    """allows access only to admin users"""

    def has_permission(self, request: Request, view) -> bool:
        return request.user.id is None


class AllowAny(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return True
