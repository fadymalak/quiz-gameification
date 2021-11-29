
from rest_framework.viewsets import ModelViewSet
from ..models import User
from django.db.models import Q
from ..serializers.user_serializers import UserSerializer,UserDetailsSerializer
from rest_framework.renderers import JSONOpenAPIRenderer,BrowsableAPIRenderer,TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny


class UserViewSet(ModelViewSet):
    renderer_classes = [BrowsableAPIRenderer,]
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            permission_classes = [IsAuthenticated]#IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes=[AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list','create','destroy']:
            # limit Access to User(last_name,first_name,username)
            return UserSerializer
        elif self.action == "update":
            # Full Access To User Data
            return UserDetailsSerializer

    def get_queryset(self):
        params = self.request.query_params
        search = params['search']
        return User.objects.filter(
            Q(username__contains=search) 
            | Q(last_name__contains=search) 
            | Q(first_name__contains=search))


