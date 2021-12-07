from rest_framework.permissions import BasePermission , SAFE_METHODS
from myapi.models import User

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        # user = User.objects.get(id =request.user.id)
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user

class IsEnrolled(BasePermission):
    def has_permission(self, request, view):
        # user = User.objects.get(id =request.user.id)
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET"]:
            #Note:Founded in Docs
            exist = request.user.courses.filter(id=obj.id).exists()
            return exist
        return False
# class IsEnrolledOrTeacher(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if request.method in SAFE_METHODS:
#             return True

#         #Allow POST For Is_staff
#         return user.is_staff

#     def has_object_permission(self, request, view, obj):
#         print(request.user)
#         if request.method in ["GET"]:
#             #Note:Founded in Docs
#             exist = request.user.courses.filter(id=obj.id).exists()
#             return (obj.owner == request.user) or exist
#         else:
#             print(obj.owner == request.user)
#             return obj.owner == request.user