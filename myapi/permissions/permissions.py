from numpy import isin
from rest_framework.permissions import BasePermission, SAFE_METHODS
from myapi.models import Quiz, User, Courses
from myapi.permissions.main import Permission
from django.urls import resolve

from myapi.serializers.quiz_serializers import Question

def _check_owner(model,instance_id : int ,user_id : int) -> bool:
    m = model.objects.get(id=instance_id)
    print(m.owner.id)
    print(user_id)
    return user_id == m.owner.id

def _check_object_owner(obj,user):
    return obj.owner == user

def _check_enrolled(user:User,instance_id:int) -> bool :
    query = user.courses.filter(id = instance_id)
    print("#instance id ",instance_id)

    print(query.count())
    exist = query.exists()
    return exist

def _check_superuser(user:User) -> bool :
    return user.is_superuser

def _check_teacher(user:User) -> bool :
    return user.is_staff
student_not_enrolled = ['list_course']
student_enrolled =  \
    ['view_course','view_quiz','list_quiz','create_answer','view_answer']
owner = student_enrolled + ['delete_course','edit_course',\
    'delete_quiz','edit_quiz','edit_answer','delete_answer']

# class StudentPerm(Permission):
#     def check_permission(self, request, action, obj):
        

class IsStudentEnroll(Permission):
    def check_permission(self, request, action, obj):
        if isinstance(obj,Courses):
            id = obj.id
        elif isinstance(obj,Quiz):
            id = obj.course.id
        elif isinstance(obj,Question):
            id = obj.quiz.course
        print(id)
        return _check_enrolled(request.user,id)


class IsCourseOwner2(Permission):
    def check_permission(self, request, action, obj):
        return _check_object_owner(obj,request.user.id)

class IsQuizOwner2(Permission):
    def check_permission(self, request, action, obj):
        id = resolve(request.path_info).kwargs['quiz_id']
        return _check_owner(Quiz,id,request.user.id)

class IsSuperUser(Permission):
    def check_permission(self, request, action, obj):
        return _check_superuser(request.user)

class IsRegistered(Permission):
    def check_permission(self, request, action=None, obj=None):
        return request.user.is_authenticated

class IsTeacher(Permission):
    def check_permission(self, request, action=None, obj=None):
        return _check_teacher(request.user)

class IsAnswerOwner(Permission):
    def check_permission(self, request, action=None, obj=None):
        return obj.user == request.user

class CoursePermission:
    list_course = IsRegistered()
    view_course = IsStudentEnroll() | IsCourseOwner2() |  IsSuperUser()
    create_course = IsTeacher() | IsSuperUser()
    edit_course = IsCourseOwner2() | IsSuperUser() 
    delete_course = IsCourseOwner2() | IsSuperUser()
    approval_course = IsSuperUser()

class QuizPermission:
    list_quiz = IsStudentEnroll() | IsCourseOwner2() | IsSuperUser()
    view_quiz =  IsStudentEnroll() | IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    create_quiz = IsCourseOwner2() |  IsSuperUser()
    edit_quiz = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    delete_quiz = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    approval_quiz =  IsCourseOwner2() | IsSuperUser()

class AnswerPermission:
    create_answer = IsStudentEnroll()
    list_answer = IsStudentEnroll() | IsAnswerOwner() |IsCourseOwner2()| IsQuizOwner2() | IsSuperUser()
    view_answer = IsAnswerOwner() |  IsCourseOwner2()| IsQuizOwner2() | IsSuperUser()
    delete_answer = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()

class QuestionPermission:
    list_question = IsStudentEnroll() | IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    view_question = IsStudentEnroll() | IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    create_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    edit_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    delete_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    approval_qeustion =  IsCourseOwner2() | IsSuperUser()
