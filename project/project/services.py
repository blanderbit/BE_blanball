from authentication.models import User
from notifications.tasks import send_to_user
from .constaints import  *
from events.models import Event

from django_filters import rest_framework as filters

from rest_framework import mixins,pagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView



class EventDateTimeRangeFilter(filters.FilterSet):
    date_and_time = filters.DateFromToRangeFilter()

    class Meta:
        model = Event
        fields = ('date_and_time',)

class UserAgeRangeFilter(filters.FilterSet):
    profile__age = filters.RangeFilter()

    class Meta:
        model = User
        fields = ('profile__age',)


def send_notification_to_event_author(event) -> None:
    if event.amount_members > event.count_current_users:
        user_type:str = 'новий'
    elif event.amount_members == event.count_current_users:
        user_type:str = 'останній'
    send_to_user(user = User.objects.get(id = event.author.id),notification_text=
        NEW_USER_ON_THE_EVENT_NOTIFICATION.format(author_name = event.author.profile.name,user_type=user_type,event_id = event.id),
        message_type=NEW_USER_ON_THE_EVENT_MESSAGE_TYPE)


class GetPutDeleteAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    '''сoncrete view for get,put or deleting a model instance'''
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PutAPIView(mixins.UpdateModelMixin,
                    GenericAPIView):
    '''concrete view for put a model instance'''
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



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
