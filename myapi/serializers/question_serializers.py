from rest_framework import serializers
from ..models2 import *
from myapi.models import User
from abc import ABC , abstractmethod
import json
from .user_serializers import UserDetailsSerializer , UserSerializer
import dataclasses
import typing
import serpyco

class UserQuestionSerializer(serializers.Serializer):
    pass

class BaseItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    deleted = serializers.IntegerField()
    title = serializers.CharField()
    image = serializers.ImageField()
    owner = serializers.CharField()#UserSerializer()

    class Meta:
        abstract = True

    @staticmethod
    def typ():
        pass

    def update(self, instance, validated_data):
        try:
            validated_data.pop("owner")
        except:
            pass
        for k,v in validated_data.items():
            setattr(instance,k,v)
        instance.save()
        return instance

class MCQSerializer(BaseItemSerializer):
    option1= serializers.CharField()
    option2= serializers.CharField()
    option3= serializers.CharField()
    option4= serializers.CharField()
    type = serializers.ReadOnlyField(default="mcq")


    @staticmethod
    def typ():
        return MCQ


    def update(self, instance, validated_data):
        try:
            validated_data.pop("owner")
        except:
            pass
        for k,v in validated_data.items():
            setattr(instance,k,v)
        instance.save()
        return instance

class YNQSerializer(BaseItemSerializer):
    type = serializers.ReadOnlyField(default="ynq")
    
    @staticmethod
    def typ():
        return YNQ

    def validate_image(self, value):
        return value
class GQSerializer(BaseItemSerializer):
    type = serializers.ReadOnlyField(default="gq")

    @staticmethod
    def typ():
        return GQ

    def validate_image(self, value):
        return value

class QuestionField(serializers.RelatedField):
    def to_representation(self, value):
        username = value.owner.username
        for serial in BaseItemSerializer.__subclasses__():
            try:
                if value['type'].lower() in serial.__name__.lower(): #isinstance(value,serial.typ()):
                    result =  serial(instance=value).data
                    result['owner'] = username
                    return result

            except:
                if isinstance(value,serial.typ()):
                    result=  serial(instance=value).data
                    result['owner'] = username
                    return result
            
        return str("{'error':'wrong class'}")

    def to_internal_value(self, data):
        user = User.objects.get(username=data["owner"])
        data['owner'] = user
        return data

    def get_queryset(self):
        return super().get_queryset()

class QuestionSerializer(serializers.ModelSerializer):
    item = QuestionField()

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        print("-> , ",data['item'])
        
        return data
    class Meta:
        model = Question
        fields = ["quiz","point","item","id"]
        
    def create(self, validated_data):
        item_data = validated_data['item']
        item_type = item_data.pop("type").lower()
        item = ""
        for i in BaseItem.__subclasses__():
            if item_type in i.__name__.lower():
                item = i(**item_data)
                item.save()
        question = Question(item=item,quiz=validated_data['quiz'],\
            point = validated_data['point'])
        question.save()
        return question

    
    def update(self, instance, validated_data):
        if validated_data.get("item"):
            item = validated_data.pop("item")
            item_type = item.pop("type")
            question = ""
            item.pop("image")
            item.pop("owner")
            for i in BaseItemSerializer.__subclasses__():
                if item_type.lower() in i.__name__.lower():

                    question_model  = i.typ().objects.get(id = item['id'])
                    question = i(question_model,data=item,partial=True)
                    question.is_valid(raise_exception=True)
                    question.save() 
                    question_model.refresh_from_db()
                    item = question_model
        else:
            item = instance.item
        point = validated_data.get("point",instance.point)
        quiz = validated_data.get("quiz",instance.quiz)
        # validated_data.pop("item")
        for k,v in validated_data.items():
            setattr(instance,k,v)
        instance.item = item
        instance.save()
        return instance
