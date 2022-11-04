from typing import Optional, Union, final

from rest_framework.exceptions import APIException

from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)
from django.utils.encoding import force_str

@final
class _404(APIException):

    status_code: int = HTTP_404_NOT_FOUND
    default_detail: str = 'Not found.'

    def __init__(self):
        detail = force_str(self.default_detail)
        super().__init__(detail)

@final
class _403(APIException):
    status_code: int = HTTP_403_FORBIDDEN
    default_detail: str = 'You cannot take this action.'