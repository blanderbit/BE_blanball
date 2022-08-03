from rest_framework import generics,permissions,filters
from .models import *
from .serializers import *
from project.services import GetPutDeleteAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

class CreateIvent(generics.CreateAPIView):
    serializer_class = IventSerializer
    # permission_classes = []
    queryset = Ivent.objects.all()

class GetPutDeleteIvent(GetPutDeleteAPIView):
    serializer_class = IventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ivent.objects.all()

class IventList(generics.ListAPIView):
    serializer_class = IventSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ['id','name','small_disc','price','place','date_and_time','amount_members']
    filterset_fields = ['type', 'need_ball','gender']
    queryset = Ivent.objects.all()

class DeleteIvents(generics.GenericAPIView):
    serializer_class = DeleteIventsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        for i in range(len(serializer.validated_data["dele"])):
            v_data = serializer.validated_data["dele"] 
            Ivent.objects.filter(id = serializer.validated_data["dele"][i]).delete()
        return Response(f"{{ivents{v_data} have been removed}}")

