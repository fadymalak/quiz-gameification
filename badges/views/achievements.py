from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404 
from rest_framework.viewsets import ModelViewSet
from badges.serializers import *
from rest_framework.permissions import IsAuthenticated
from badges.permission import IsOwner
from badges.usecase.achievement import create_achievement,create_achievement_level,update_achievement,update_achievement_level,get_achievement,get_achievement_level
# Create your views here.
REQUIRED_OWNER = ["create", "destroy", "update", "partial_update"]

class AchievementViewSet(ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def retrieve(self, request,pk, *args, **kwargs):
        obj = get_achievement(ach_id=pk)
        res = self.get_serializer(obj)
        return Response(data=res.data,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data =request.data
        serializer = self.get_serializer(data=data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        obj ,created = create_achievement(name=serializer.validated_data['name'],owner=request.user)
        res = self.get_serializer(obj)
        return Response(res.data,status=201)

    def partial_update(self, request, pk=None,*args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        obj = update_achievement(name=serializer.validated_data['name'],ach_id=pk)
        res = self.get_serializer(obj)
        return Response(res.data , status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class AchievementLevelViewSet(ModelViewSet):
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
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return AchievementLevelReadSerializer
        return AchievementLevelSerializer


    def create(self, request, *args, **kwargs):
        """
        Create new Achievement Level

        `data` 
        * data
        * data2
        """
        ach_id = kwargs.get("achievement_pk")
        data = request.data
        user = request.user

        print(self.get_serializer_class())
        serializer = self.get_serializer(data=data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        obj,created = create_achievement_level(
            ach_id,
            data=serializer.validated_data,
            owner=user
            )
        res = AchievementLevelReadSerializer(obj)
    
        return Response(res.data,status=status.HTTP_201_CREATED)

    def retrieve(self, request,pk, *args, **kwargs):
        obj = get_achievement_level(ach_l_id=pk)
        res = self.get_serializer(obj)
        return Response(res.data,status= status.HTTP_200_OK)

    def partial_update(self, request, pk,*args, **kwargs):
        data = request.data
        obj = update_achievement_level(ach_l_id=pk,data=data)
        res = self.get_serializer(obj)
        return Response(res.data,status=status.HTTP_200_OK)
