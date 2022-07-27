
from myapi.services.service import Service
from myapi.models import Courses
# from myapi.serializers.course_serializers import CourseDetailSerializer ,CourseSerializers 
from typing import Union
from django.db.models import Q , F ,Value
from django.db.models.functions import Concat
from django.db.models import QuerySet
class CourseService(Service):
    
    def get_by_id(id:int , detail: bool = False) :
        course  = Courses.objects.get(id=id)
        return course
    def get_by_id_o(id:int) -> Courses :
        course = Courses.objects.get(id=id)
        return course
        
    def get_courses_by_name(name:str) -> QuerySet[Courses]:
        if name is not None :
            courses = Courses.objects.filter(name__contains=name).all()
        else : 
            courses = QuerySet(Courses)
        return courses
        
    def get_courses_by_teacher(name:str)-> QuerySet[Courses]:
        if name is not None :
            courses = Courses.objects.select_related("owner").alias(oname=Concat(F('owner__first_name'),Value(" "),F("owner__last_name"))).filter(Q(owner__first_name__contains=name)|\
                Q(owner__last_name__contains=name)|\
                    Q(oname__contains=name)|\
                        Q(owner__username__contains=name)).all()
        else:
            courses = QuerySet(Courses)
        return courses

    def create(owner,**kwargs) :
        course = Courses.objects.create(owner=owner,**kwargs)
        return course

    def update(course:Courses ,**kwargs) :
        updated = 0
        for k,v in kwargs.items():
            if getattr(course,k) != v :
               setattr(course,k,v)
               updated= 1
        course.save()
        return  course
            
    def delete(course_id):
        course = Courses.objects.get(id=course_id).delete()
        return course
