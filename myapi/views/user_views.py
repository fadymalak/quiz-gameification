from rest_framework.viewsets import ModelViewSet

from myapi.serializers.user_serializers import UserSerial
from ..models import User
from django.db.models import Q


from rest_framework.decorators import permission_classes, action
from myapi.views.view import CustomViewset
from myapi.mixin import ObjectMixin,CustomDispatchMixin
from myapi.services.user import UserService
from myapi.permissions.permissions import UserPermission
from rest_framework.exceptions import MethodNotAllowed
from myapi.usecase.user import user_update , create_user
from rest_framework.response import Response
from rest_framework import status
class UserViewSet(CustomDispatchMixin,CustomViewset):
    model = User
    service = UserService
    pk_url_kwarg = "pk"
    permission = UserPermission

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_permission("view_user",request)
        return Response(UserSerial.dump(user),status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        query= self.request.query_params
        self.check_permission("list_user",request)
        users  = UserService.get_users_by_name(query['name'])
        users = [user for user in users]
        return Response(UserSerial.dump(users,many=True),status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        data = request.data
        user = self.get_object()
        self.check_permission("edit_user",request,obj=user)
        user = user_update(user,**data)
        return Response(UserSerial.dump(user),status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        self.check_permission("create_user",request)
        user = create_user(**data)
        return Response(data=UserSerial.dump(user),status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(detail="method not allowed")
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        self.check_permission("delete_user",request,obj=user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class UserViewSet2(ModelViewSet):
    # renderer_classes = [
        # BrowsableAPIRenderer,
    # ]
 #   serializer_class = UserSerializer
# 
    # def get_permissions(self):
        # if self.action in ["list", "retrieve"]:
            # permission_classes = [IsAuthenticated]  # IsAuthenticatedOrReadOnly]
        # elif self.action == "create":
            # permission_classes = [AllowAny]
        # else:
            # permission_classes = [IsSameUser]
        # return [permission() for permission in permission_classes]
# 
    #def get_serializer_class(self):
    #    if self.action in ["list", "create", "destroy"]:
    #        # limit Access to User(last_name,first_name,username)
    #        return UserSerializer
    #    elif self.action == "update":
    #        # Full Access To User Data
    #        return UserDetailsSerializer

    # def get_queryset(self):
        # params = self.request.query_params
        # search = params["search"]
        # return User.objects.filter(
            # Q(username__contains=search)
            # | Q(last_name__contains=search)
            # | Q(first_name__contains=search)
        # )
# 