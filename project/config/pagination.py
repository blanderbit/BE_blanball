from collections import OrderedDict
from functools import wraps
from typing import Any, Optional, Callable

from django.conf import settings
from rest_framework.pagination import (
    PageNumberPagination,
)
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size = settings.PAGINATION_PAGE_SIZE

    def get_paginated_response(self, results: dict[str, Any]) -> Response:
        response_data = OrderedDict(
            [
                ("total_count", self.page.paginator.count),
                ("page_size", self.page_size),
                ("current_page", self.page.number),
                ("next", self.get_next_link() or None),
                ("previous", self.get_previous_link() or None),
                ("success", True),
                ("results", results),
            ]
        )
        return Response(response_data)



def paginate_by_offset(cls: type) -> type:
    original_get_queryset = cls.get_queryset

    @wraps(original_get_queryset)
    def new_get_queryset(self, *args, **kwargs):
        offset = self.request.query_params.get("offset")
        if offset is not None:
            try:
                offset = int(offset)
                if offset < 0:
                    offset = self.pagination_class.page_size
            except ValueError:
                offset = None
        if offset is not None:
            self.pagination_class.page_size = offset
        else:
            self.pagination_class.page_size = settings.PAGINATION_PAGE_SIZE
        return original_get_queryset(self, *args, **kwargs)

    cls.get_queryset = new_get_queryset
    return cls