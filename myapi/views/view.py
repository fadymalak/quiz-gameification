from typing import List
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from django.views.generic.detail import SingleObjectMixin
from myapi.mixin import PermissionMixin
from myapi.services.service import Service
from myapi.permissions.permissions import Permission
from rest_framework.renderers import JSONRenderer
from django.db.models import Model
from abc import ABC , abstractmethod
class AbsViewset(ABC):

    @abstractmethod
    def create(self,request,*args,**kwargs):
        pass

    @abstractmethod
    def update(self,request,*args,**kwargs):
        pass

    @abstractmethod
    def partial_update(self,request,*args,**kwargs):
        pass

    @abstractmethod
    def destroy(self,request,*args,**kwargs):
        pass
    

class CustomViewset(PermissionMixin,SingleObjectMixin,ViewSet):
    service : Service = None
    permission : Permission = None
    renderer_classes : List = [JSONRenderer,]
    model : Model  = None
    pk_url_kwarg : str = "pk"


    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
    # def retrieve(self, request, *args, **kwargs):
        # return super().get(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return super().put(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     return super().patch(request, *args, **kwargs)
    
    # def destroy(self, request, *args, **kwargs):
    #     return super().delete(request, *args, **kwargs)