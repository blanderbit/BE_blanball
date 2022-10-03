from authentication.models import User
from notifications.tasks import send_to_user
from .constaints import  *
from events.models import Event

from rest_framework import mixins,pagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data) -> Response:
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
