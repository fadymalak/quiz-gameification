from os import stat
from itsdangerous import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from badges.models import AchievementLevel, Rules
from badges.permission import IsOwner
from badges.rule_serializer import RulesSerializer
from rest_framework.permissions import AllowAny , IsAuthenticated


from badges.views import achievements
# from django.db.models import 

class RulesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RulesSerializer

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    def list(self, request, achievement_level_pk=None):
        achievement_level = AchievementLevel.objects.get(id=achievement_level_pk)
        rules = achievement_level.rules.all()
        serializer = Rules(rules,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def retrieve(self, request,achievement_level_pk=None,pk=None):
        rule  = Rules.objects.get(id=pk)
        serializer = RulesSerializer(rule)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        print(self.kwargs)
        data['achievement_level'] = self.kwargs['achievement_level_pk']
        serializer = RulesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

