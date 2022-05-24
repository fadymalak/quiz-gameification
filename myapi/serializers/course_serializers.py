from datetime import datetime
from rest_framework import serializers
from myapi.models import Courses
from serpyco import Serializer
from dataclasses import dataclass
from myapi.serializers.user_serializers import User
from myapi.serializers.serial import ID , CreatedAt

@dataclass
class CourseId:
    id : int

@dataclass
class Course(ID,CreatedAt):
    name : str
    owner : User
    
CourseSerial = Serializer(Course)

class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["owner", "name"]


class CourseDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Courses
        exclude = ["id"]
