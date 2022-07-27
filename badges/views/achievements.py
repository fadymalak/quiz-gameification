from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404 
from rest_framework.viewsets import ModelViewSet
from badges.serializers import *
from rest_framework.permissions import IsAuthenticated
from badges.permission import IsOwner
# Create your views here.
REQUIRED_OWNER = ["create", "destroy", "update", "partial_update"]

class AchievementViewSet(ModelViewSet):
    """
    API Endpoint 

    retrieve:
    retrieve specific AchievementLevel
    
    * data

    list:
    Return all data list

    """
    queryset = AchievementLevel.objects.all()
    serializer_class = AchievementLevelSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in REQUIRED_OWNER:
            permissions = [IsOwner,IsAuthenticated]
            return [perm() for perm in permissions]
        return super().get_permissions(self)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return AchievementLevelReadSerializer
        return AchievementLevelSerializer

    def get_create_achievement(self,data,user):
        achievement = Achievement.objects.filter(name=data['name']).all()
        if achievement:
            if achievement[0].owner == user:
                return achievement[0]
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            achievement = Achievement.objects.create(name=data['name'],owner=user)
            return achievement

        

    def create_achievement_level(self,data,user):
        achievement = Achievement.objects.filter(name=data['name']).all()
        if achievement:
            if not achievement.owner == user :
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            achievement = Achievement.objects.create(
                name=data['name'],
                owner=user
            )
        return achievement
    def create(self, request, *args, **kwargs):
        """
        Create new Achievement Level

        `data` 
        * data
        * data2
        """
        data = request.data
        print(self.get_serializer_class())
        serializer = self.get_serializer(data=data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
    
        return Response(serializer.data,status=status.HTTP_201_CREATED)