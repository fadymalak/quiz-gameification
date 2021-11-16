from rest_framework import serializers
from ..models import Courses

class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        models = Courses
        