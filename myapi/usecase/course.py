from myapi.serializers.course_serializers import Course
from myapi.services.course import CourseService
from myapi.models import Courses
from typing import List
from rest_framework.exceptions import ParseError
from itertools import chain
def course_list(query:dict) -> List[Courses]:
    search = query.get("search",None)
    if search is None :
        raise ParseError(detail="Please add filters")
    
    queryset = CourseService.get_courses_by_teacher(search)
    queryset_by_name = CourseService.get_courses_by_name(search)
    final_query = [course for course in chain(queryset,queryset_by_name)]
    return final_query

def course_create(user,**data) -> Courses :
    course = CourseService.create(owner=user,**data)
    return course

def course_update(course_id , **data):
    course = CourseService.get_by_id(course_id)
    updated_course = CourseService.update(course,**data)
    return updated_course
    

def course_delete(course):
    try:
       course.delete()
    except Exception:
        return False
    return True