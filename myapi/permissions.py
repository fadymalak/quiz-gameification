from rest_framework.permissions import BasePermission, SAFE_METHODS
from myapi.models import Quiz, User, Courses
from django.urls import resolve


class IsCourseOwner(BasePermission):
    def has_permission(self, request, view):

        course_id = request.data["course"]
        query = Courses.objects.get(id=course_id)

        return request.user.is_staff and (request.user == query.owner)


class IsQuizOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return IsCourseOwner.has_permission(self, request, view)
        pk = resolve(request.path_info).kwargs["pk"]
        print("PK -> ", pk)
        query = Quiz.objects.get(id=pk)
        print(query)
        return request.user.is_staff and (request.user == query.owner)


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
