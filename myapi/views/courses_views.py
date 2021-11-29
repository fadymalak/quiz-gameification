from rest_framework.decorators import renderer_classes
from rest_framework.viewsets import ModelViewSet
from ..models import Courses,User
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from ..serializers.course_serializers import CourseSerializers
from django.db.models import Q 

class CourseViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer,BrowsableAPIRenderer]
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset()

    def get_permissions(self):
        return super().get_permissions()

