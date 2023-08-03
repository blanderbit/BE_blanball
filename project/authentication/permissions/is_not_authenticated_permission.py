from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request


class IsNotAuthenticated(BasePermission):
    """allows access only to admin users"""

    def has_permission(self, request: Request, view) -> bool:
        return request.user.id is None
