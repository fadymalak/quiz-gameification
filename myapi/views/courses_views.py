from serpyco.validator import ValidationError
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.viewsets import ModelViewSet
from ..models import Courses, User
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
# from ..serializers.course_serializers import CourseDetailSerializer, CourseSerializers
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from rest_framework.response import Response
from rest_framework import status
from myapi.views.view import CustomViewset
from myapi.services.service import Service
from myapi.services.course import CourseService
from myapi.serializers.course_serializers import CourseSerial , CourseValidator
from myapi.permissions.permissions import CoursePermission
from myapi.usecase.course import course_create , course_delete ,course_list,course_update
from myapi.mixin import CustomDispatchMixin
from rest_framework.exceptions import ParseError
class CourseViewSet(CustomDispatchMixin,CustomViewset):
    service: Service
    pk_url_kwarg: str = "pk"
    permission = CoursePermission
    model = Courses

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        self.check_permission("view_course",request,obj=course)
        return Response(data=CourseSerial.dump(course),status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        query = request.query_params
        self.check_permission("list_course",request)
        courses = course_list(query)
        return Response(data=CourseSerial.dump(courses,many=True),status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            CourseValidator.validate(data)
        except ValidationError:
            
            raise ParseError(detail="invaild data")
        self.check_permission("create_course",request)
        course = course_create(user=request.user,**data)
        return Response(data=CourseSerial.dump(course),status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        course_id = self.kwargs[self.pk_url_kwarg]
        course= self.get_object()
        try:
            CourseValidator.validate(data)
        except ValidationError:
            raise ParseError(detail="invalid data")
        self.check_permission("edit_course",request,obj=course)
        course = course_update(course_id,**data)
        return Response(data=CourseSerial.dump(course),status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        course_id = self.kwargs[self.pk_url_kwarg]
        course = self.get_object()
        self.check_permission("delete_course",request,obj=course)
        course_delete(course=course)
        return Response(status = status.HTTP_204_NO_CONTENT)