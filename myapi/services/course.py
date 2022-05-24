
from myapi.services.service import Service
from myapi.models import Courses
from myapi.serializers.course_serializers import CourseDetailSerializer ,CourseSerializers 
from typing import Union

class CourseService(Service):
    
    def get_by_id(id:int , detail: bool = False) -> Union[CourseDetailSerializer,CourseSerializers]:
        course  = Courses.objects.get(id=id)
        if detail:
            return CourseDetailSerializer(course)
        return  CourseSerializers(course)

    def get_by_id_o(id:int) -> Courses :
        course = Courses.objects.get(id=id)
        return course

    def create(**kwargs) -> CourseDetailSerializer:
        course = Courses.objects.create(**kwargs)
        return CourseDetailSerializer(course)

    def update(course:Courses ,**kwargs) -> CourseDetailSerializer:
        updated = 0
        for k,v in kwargs.items():
            if getattr(course,k) != v :
               setattr(course,k,v)
               updated= 1
        course.save()
        return  CourseDetailSerializer(course)
            

