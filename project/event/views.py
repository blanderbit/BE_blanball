from rest_framework import generics,permissions,filters
from .models import *
from .serializers import *
from project.services import GetPutDeleteAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

class CreateEvent(generics.CreateAPIView):
    '''class that allows you to create a new event'''
    serializer_class = EventSerializer
    # permission_classes = []
    queryset = Event.objects.all()

class GetPutDeleteEvent(GetPutDeleteAPIView):
    '''a class that allows you to get, update, delete an event'''
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()

class EventList(generics.ListAPIView):
    '''class that allows you to get a complete list of events'''
    serializer_class = EventListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ['id','name','small_disc','price','place','date_and_time','amount_members']
    filterset_fields = ['type', 'need_ball','gender']
    queryset = Event.objects.all()

class DeleteEvents(generics.GenericAPIView):
    '''class that allows you to delete multiple events at once'''
    serializer_class = DeleteIventsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        for i in range(len(serializer.validated_data["dele"])):
            v_data = serializer.validated_data["dele"] 
            Event.objects.filter(id = serializer.validated_data["dele"][i]).delete()
        return Response(f"{{ivents{v_data} have been removed}}")

