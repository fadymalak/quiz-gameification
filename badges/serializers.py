from badges.models import *
from rest_framework import serializers
from myapi.serializers.user_serializers import * 
from badges.rule_serializer import RulesSerializer
from rest_framework.fields import SkipField
from serpy import StrField
from serpy import Serializer

class Username(Serializer):
    username = StrField()
    
class SubAchievementLevelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    image = models.URLField()
    class Meta:
        model = AchievementLevel
        fields = ("name","image")


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username']

class AchievementNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ['name']


class AchievementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    owner = UsernameSerializer()
    class Meta:
        model = Achievement
        fields = "__all__"


class AchievementLevelReadSerializer(serializers.ModelSerializer):
    owner = UsernameSerializer()
    parent = SubAchievementLevelSerializer()
    rules = RulesSerializer(many=True,read_only=True)
    class Meta:
        model = AchievementLevel
        fields = "__all__"
        
class AchievementLevelSerializer(serializers.ModelSerializer):
    achievement = AchievementNameSerializer()
    image = serializers.ImageField(required=False)
    owner = UsernameSerializer(read_only=True)
    class Meta:
        model = AchievementLevel
        fields = "__all__"

    def create(self, validated_data):
        print("inside create")
        print(validated_data)
        owner = self.context['request'].user
        achievement = validated_data.pop('achievement')
        #TODO when create GroupAdmin  change owner
        achievement,created = Achievement.objects.get_or_create(**achievement,owner=owner)

        instance = AchievementLevel.objects.create(achievement=achievement,owner=owner,**validated_data)
        print("created")
        return instance

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()
    user =UsernameSerializer()
    class Meta:
        model = UserAchievement
        fields = "__all__"



class VariableUserSerializer(serializers.ModelSerializer):
    user = UsernameSerializer()
    class Meta:
        model = VariableUser
        fields = "__all__"


class VariableUserDetialsSerializer(serializers.ModelSerializer):
    variable_user = VariableUserSerializer()
    class Meta:
        model = VariableUserDetials
        fields = "__all__"


