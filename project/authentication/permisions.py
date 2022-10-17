from typing import Optional, Literal

from rest_framework import permissions
from rest_framework.request import Request

class IsNotAuthenticated(permissions.BasePermission):
    '''allows access only to not auth users'''
    def has_permission(self, request: Request, view) -> Optional[Literal[True]]:
        if request.user.id == None:
            return True
