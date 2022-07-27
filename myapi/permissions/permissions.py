from myapi.models import Quiz, User, Courses
from myapi.permissions.main import Permission
from django.urls import resolve

from myapi.serializers.quiz_serializers import Question

def _check_owner(model,instance_id : int ,user_id : int) -> bool:
    m = model.objects.get(id=instance_id)
    return user_id == m.owner.id

def _check_object_owner(obj,user):
    return obj.owner == user

def _get_course_object(obj):
    course = None
    if isinstance(obj,Question):
        course = obj.quiz.course
    elif isinstance(obj,Quiz):
        course = obj.course
    elif isinstance(obj,Courses):
        course = obj
    return course

def _check_enrolled(user:User,instance_id:int) -> bool :
    
    query = user.courses.filter(id = instance_id)
    print("#instance id ",instance_id)

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
        else :
            raise Exception("Object not have course attribute")
        return _check_enrolled(request.user,id)


class IsCourseOwner2(Permission):
    def check_permission(self, request, action, obj):
        course = _get_course_object(obj)
        return _check_object_owner(course,request.user)

class IsQuizOwner2(Permission):
    def check_permission(self, request, action, obj = None):

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

class IsSameUser(Permission):
    def check_permission(self, request, action=None, obj=None):
        return request.user == obj

class AllowAny(Permission):
    def check_permission(self, request, action=None, obj=None):
        print(request.user.is_anonymous)
        if request.user.is_anonymous :
            return True
class CoursePermission:
    list_course = IsRegistered()
    view_course = IsStudentEnroll() | IsCourseOwner2()  |   IsSuperUser() # | IsCourseStaff()
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
    list_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    view_question =  IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    create_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    edit_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    delete_question = IsCourseOwner2() | IsQuizOwner2() | IsSuperUser()
    approval_qeustion =  IsCourseOwner2() | IsSuperUser()


class UserPermission:
    list_user = IsRegistered() | IsSuperUser()
    view_user = IsRegistered() |  IsSuperUser()
    create_user = AllowAny()
    edit_user = IsSameUser() |  IsSuperUser()
    delete_user = IsSameUser() | IsSuperUser()
    # approval_user =  IsCourseOwner2() | IsSuperUser()
