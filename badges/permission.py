from rest_framework.permissions import BasePermission
from badges.utils import check_staff

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return check_staff(request.user,0,0)
    
    def has_object_permission(self, request, view, obj):
        return check_staff(request.user,obj.owner,0)