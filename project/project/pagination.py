from typing import Any

from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    
    page_size = settings.PAGINATION_PAGE_SIZE

    def get_paginated_response(self, data: dict[str, Any]) -> Response:
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })