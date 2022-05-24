from rest_framework.permissions import BasePermission, SAFE_METHODS
from myapi.models import Quiz, User, Courses
from django.urls import resolve

def _check_owner(model,instance_id : int ,user_id : int) -> bool:
    m = model.objects.get(id=instance_id)
    return user_id == m.owner.id

def _check_enrolled(user:User,instance_id:int) -> bool :
    exist = User.courses.filter(id = instance_id).exists()
    return exist

def _check_staff(user:User) -> bool :
    return user.is_staff

student_not_enrolled = ['list_course']
student_enrolled =  \
    ['view_course','view_quiz','list_quiz','create_answer','view_answer']
owner = student_enrolled + ['delete_course','edit_course',\
    'delete_quiz','edit_quiz','edit_answer','delete_answer']

class StudentPerm(BasePermission):
    def has_permission(self, request, view):
        
        print(f"{view.name=}")
        if view.name == 'create_answer':
            course_id = resolve(request.path_info).kwargs['course_id']
            return _check_enrolled(user=request.user,instance_id=course_id)

        if request.method ==  SAFE_METHODS :
            if view.name in student_enrolled:
                return _check_enrolled(user=request.user,instance_id=course_id)
            elif view.name == 'list_course':
                return True
        else:
            return False

class OwnerPerm(BasePermission):
    def has_permission(self, request, view):
        model = view.model
        
        return _check_staff(request.user) and _check_owner(model)
class IsCourseOwner(BasePermission):
    def has_permission(self, request, view):

        course_id = request.data["course"]
        query = Courses.objects.get(id=course_id)

        return request.user.is_staff and (request.user == query.owner)


class IsQuizOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return IsCourseOwner.has_permission(self, request, view)
        # pk = resolve(request.path_info).kwargs["pk"]
        try:
            pk = request.data['id']
        except : 
            pk = resolve(request.path_info).kwargs["quiz_id"]
        print("PK -> ", pk)
        quiz = Quiz.objects.get(id=pk)
        print(quiz.owner)
        return request.user.is_staff and (request.user == quiz.owner)


class IsSameUser(BasePermission):
    """
    For Change User Data (password,bio,image etc)
    """

    def has_permission(self, request, view):
        if request.method in ["PATCH", "PUT"]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        # user = User.objects.get(id =request.user.id)
        #TODO allow access others quizs `permission_issue`
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user


class IsStaffx(BasePermission):
    def has_permission(self, request, view):
        print(view)
        return True

    def has_object_permission(self, request, view, obj):
        print(obj.id)
        return False


class IsEnrolled(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        req = resolve(request.path_info)
        if req.view_name == "quiz-submit_asnwer":
            quiz_id = req.kwargs["pk"]
            course = Courses.objects.filter(quizs__id=quiz_id).only("id").first()
            if request.user.courses.filter(id=course.id).exists():
                return True
            else:
                return False
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET"]:
            # Note:Founded in Docs
            exist = request.user.courses.filter(id=obj.id).exists()
            return exist
        return False


class IsEnrolledOrTeacher(BasePermission):
    def has_permission(*args, **kwargs):
        return IsEnrolled.has_permission(*args, **kwargs) or IsTeacher.has_permission(
            *args, **kwargs
        )

    def has_object_permission(*args, **kwargs):
        return IsEnrolled.has_object_permission(
            *args, **kwargs
        ) or IsTeacher.has_object_permission(*args, **kwargs)

class CoursePermission(BasePermission):
    def has_permission(self, request, view):
        course_id = resolve(request.path_info).kwargs['pk']
        user = request.user
        if user.courses.filter(id=course_id).exists():
            return True
        if user.is_staff :
            obj = Courses.objects.prefetch_related("owner").only("owner").get(id=course_id)
            if obj.owner == user:
                return True

        return False
    
    def has_object_permission(self, request, view,obj):
        print("hello")
        user = request.user
        if user.is_staff :
            if obj.owner == user:
                return True
            else:
                return False
