from rest_framework import serializers
from rest_framework.decorators import authentication_classes, permission_classes, renderer_classes
from rest_framework.viewsets import ModelViewSet
from ..models import Courses,User
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from ..serializers.course_serializers import CourseDetailSerializer, CourseSerializers
from django.db.models import Q ,Value
from django.db.models.functions import Concat 
from rest_framework.permissions import AND,OR,IsAuthenticated
from myapi.permissions import IsTeacher,IsEnrolled
from rest_framework.response import Response
from rest_framework import status

class CourseViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer,BrowsableAPIRenderer]
    permission_classes = [AND(OR(IsEnrolled,IsTeacher) , IsAuthenticated),]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CourseDetailSerializer
        return CourseSerializers

    def get_queryset(self):
        param = self.request.query_params
        # print(self.kwargs)
        search = param.get("search",self.kwargs['pk'])
        return Courses.objects.filter(
            Q(owner__first_name__contains=search) |
            Q(name__contains = search)|
            Q(id = search)
        )

    def create(self,request):
        data = request.data
        user = request.user
        print(user)
        data['owner']=user.id
        print(data)
        serializer = CourseSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            
            return Response(data=serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    
