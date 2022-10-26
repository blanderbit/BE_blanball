from typing import Any, Optional

from collections import OrderedDict

from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK



class CustomPagination(PageNumberPagination):
    
    page_size = settings.PAGINATION_PAGE_SIZE

    def get_paginated_response(self, results: dict[str, Any]) -> Response:
        response_data = OrderedDict([
            ('total_count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('current_page', self.page.number),
            ('next', self.get_next_link() or None),
            ('previous', self.get_previous_link() or None),
            ('status', HTTP_200_OK),
            ('message', ('Success')),
            ('success', True),
            ('results', results)
        ])
        return Response(response_data)