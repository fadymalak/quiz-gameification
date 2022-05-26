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
    def post(self,request,*args,**kwargs):
        pass

    @abstractmethod
    def put(self,request,*args,**kwargs):
        pass

    @abstractmethod
    def patch(self,request,*args,**kwargs):
        pass

    @abstractmethod
    def delete(self,request,*args,**kwargs):
        pass
    

class CustomViewset(PermissionMixin,SingleObjectMixin,ListAPIView,ViewSet,AbsViewset):
    service : Service = None
    permission : Permission = None
    renderer_classes : List = [JSONRenderer,]
    model : Model  = None
    pk_url_kwarg : str = None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)