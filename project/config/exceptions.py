from typing import Optional, Union, final

from django.utils.encoding import force_str
from rest_framework.exceptions import APIException
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


@final
class _404(APIException):

    status_code: int = HTTP_404_NOT_FOUND
    default_detail: str = "{object_name}_not_found"

    def __init__(self, *, object=None, detail: Optional[Union[dict[str, str]]] = None):
        if object is None and detail is None:
            raise Exception("detail or object must be set")
        if detail is None:
            detail = force_str(self.default_detail).format(object_name=object.__name__.lower())
        super().__init__(detail)
