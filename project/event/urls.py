from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one event 
    path('client/event/create',CreateEvent.as_view(),
        name = 'create-event'),
    #endpoint where a user with admin
    #role can get detail info,update and delete event 
    path('admin/event/<int:pk>',GetPutDeleteEvent.as_view(),
        name = 'event-detail'),
    #endpoint where a use can get list of events
    path('client/event/list',EventList.as_view(),
        name = 'event-list'),
    #endpoint where a user with admin
    #role can delete events
    path('client/events/delete',DeleteEvents.as_view(),
        name = 'events-delete'),
]
