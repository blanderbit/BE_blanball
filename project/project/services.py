from rest_framework import mixins
from rest_framework.generics import GenericAPIView


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