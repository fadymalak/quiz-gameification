from datetime import datetime
from myapi.models import Courses
from serpyco import Serializer ,string_field , AbstractValidator , SchemaBuilder
from dataclasses import dataclass
from serpyco.validator import ValidationError
from myapi.serializers.user_serializers import User
from myapi.serializers.serial import ID , CreatedAt , Validator
from typing import Optional
@dataclass
class CourseId:
    id : int

@dataclass
class Course(ID,CreatedAt):
    name : str
    owner : Optional[User] = ''
    
@dataclass 
class CourseCreate:
    name:str = string_field(min_length=4)




_CourseCreateSchema = SchemaBuilder(CourseCreate)
CourseValidator = Validator(schema_builder=_CourseCreateSchema)
CourseCreateSerial = Serializer(CourseCreate)
CourseSerial = Serializer(Course)
# 
# class CourseSerializers(serializers.ModelSerializer):
    # class Meta:
        # model = Courses
        # fields = ["owner", "name"]
# 

# class CourseDetailSerializer(serializers.ModelSerializer):
    # owner = serializers.SlugRelatedField(slug_field="username", read_only=True)
# 
    # class Meta:
        # model = Courses
        # exclude = ["id"]
