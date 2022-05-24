from datetime import datetime
from rest_framework import serializers
# from myapi.models import Quiz, Answer
from myapi.serializers.question_serializers import QuestionSerializer
from django.db.models.manager import Manager

from serpyco import Serializer ,post_dump,post_load ,pre_dump
from dataclasses import dataclass
from typing import Callable, List, Union , Optional 
from myapi.serializers.user_serializers import User 
from myapi.serializers.course_serializers import CourseId
from myapi.serializers.serial import ID , CreatedAt


@dataclass 
class Quiz(ID,CreatedAt):
    title : str
    owner : User
    end_at : datetime
    course : CourseId



@dataclass
class QuestionBase(ID,CreatedAt):
    title : str
    image : str
    owner : User

@dataclass
class Correct:
    correct_answer : str
@dataclass
class YNQ(QuestionBase,Correct):
    pass


@dataclass
class GQ(QuestionBase,Correct):
    pass

@dataclass
class MCQ(QuestionBase,Correct):
    option1 : str
    option2 : str
    option3 : str
    option4 : str

@dataclass
class Question(ID):
    quiz : Quiz
    deleted : int
    point : int
    item : Union[MCQ,GQ,YNQ]



@dataclass
class Answer(ID,CreatedAt):
    point : int
    user : User
    question : Question
    user_answer : str
    status : str

QuestionSerial = Serializer(Question)
@dataclass
class QuizDetail(Quiz):
    questions:str

    @post_dump
    def ob(data) :
        data['questions'] = [QuestionSerial.dump(i) for i in data['questions'].all()]
        return data

QuizSerial = Serializer(Quiz)
QuizDetailSerial = Serializer(QuizDetail)
AnswerSerial = Serializer(Answer)
QuestionSerial = Serializer(Question)
YNQSerial = Serializer(YNQ)
GQSerial = Serializer(GQ)
MCQSerial = Serializer(MCQ)

#class QuizSerializers(serializers.ModelSerializer):
#
#    class Meta:
#        model = Quiz
#        depth = 0
#        exclude = ["users"]
#
#
#class QuizDetailSerializer(serializers.ModelSerializer):
#    questions = QuestionSerializer(many=True, read_only=True)
#
#    class Meta:
#        model = Quiz
#        depth = 1
#        exclude = ["users", "owner", "end_at"]
#
#
#class AnswerSerializer(serializers.ModelSerializer):
#    '''
#    used for deserialize single question answer
#    '''
#    class Meta:
#        model = Answer
#        exclude = ["created_at", "id"]
#
#
#