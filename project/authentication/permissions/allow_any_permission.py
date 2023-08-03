from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request


class AllowAny(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return True
