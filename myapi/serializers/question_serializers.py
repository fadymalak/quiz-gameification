from rest_framework import serializers
from ..models2 import *
from abc import ABC , abstractmethod
import json
from .user_serializers import UserDetailsSerializer , UserSerializer
import dataclasses
import typing
import serpyco



class BaseItemSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    deleted = serializers.IntegerField()
    title = serializers.CharField()
    image = models.ImageField()
    owner = UserSerializer()

    class Meta:
        abstract = True

    @staticmethod
    def typ():
        pass

class MCQSerializer(BaseItemSerializer):
    option1= serializers.CharField()
    option2= serializers.CharField()
    option3= serializers.CharField()
    option4= serializers.CharField()
    # correct_answer = serializers.CharField()
    type = serializers.ReadOnlyField(default="mcq")

    @staticmethod
    def typ():
        return MCQ

class YNQSerializer(BaseItemSerializer):
    # correct_answer = serializers.CharField()
    type = serializers.ReadOnlyField(default="ynq")
    
    @staticmethod
    def typ():
        return YNQ

class GQSerializer(BaseItemSerializer):
    # correct_answer = serializers.CharField()
    type = serializers.ReadOnlyField(default="gq")

    @staticmethod
    def typ():
        return GQ


class QuestionField(serializers.RelatedField):
    def to_representation(self, value):
        for serial in BaseItemSerializer.__subclasses__():
            if isinstance(value,serial.typ()):
                return serial(instance=value).data

        
        return str("{'error':'wrong class'}")
class QuestionSerializer(serializers.Serializer):
    item = QuestionField(read_only=True)
    qid = serializers.IntegerField()

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        # data['type'] = 
        type = data['item'].pop("type")
        data['type'] = type

        return data
    class Meta:
        model = Question
        fields = '__all__'
        