from django.http import Http404
from rest_framework.exceptions import PermissionDenied,AuthenticationFailed
from django.urls import resolve
class PermissionMixin:
    # def check_permission(self,request,action=None,obj=None):
        # vaild = self.permission.check_permission(request,action,obj)
        # print(vaild)
        # if not vaild : 
            # raise PermissionDenied
        # return 
    def check_permission(self,permission,request=None,action=None,obj=None):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            raise PermissionDenied
        permcls = getattr(self.permission,permission)
        vaild = permcls.check_permission(request,action,obj)
        if not vaild :
            raise PermissionDenied

class OnlyUserMixin:
    def perform_authentication(self, request):
        if request.user.is_anonymous:
            raise AuthenticationFailed('Please login')
  
class ObjectMixin:

    def get_object(self,request):
        try:
            obj_id = resolve(request.path_info).kwargs[self.pk]
        except:
            obj_id = request.data['id']
        obj = self.service.get_by_id(obj_id)
        return obj

class CustomDispatchMixin:

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                if request.method.lower() == "get":
                    
                    if len(self.kwargs.get("answer_id")) != 0:
                        handler = getattr(self, "get",
                                  self.http_method_not_allowed)
                    else:
                        handler = getattr(self, "list",
                                  self.http_method_not_allowed)
                else:


                    handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response