from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one event 
    path('client/event/create',CreateEvent.as_view(),
        name = 'create-event'),
    #endpoint where a user with admin
    #role can get detail info,update and delete event 
    path('client/event/<int:pk>',GetPutDeleteEvent.as_view(),
        name = 'event-detail'),
    #endpoint where a use can get list of events
    path('client/event/list',EventList.as_view(),
        name = 'event-list'),
    #endpoint where a user with admin
    #role can delete events
    path('admin/events/delete',DeleteEvents.as_view(),
        name = 'events-delete'),
    #endpoint where a user can join to event 
    path('client/event/join',JoinToEvent.as_view(),
        name = 'event-join'),
    #endpoint where a user can leaver from event 
    path('client/event/leave',LeaveFromEvent.as_view(),
        name = 'event-leave'),
    #endpoint where a use can get list of user events
    path('client/my/events/list',UserEvents.as_view(),
        name = 'events-list'),
]
