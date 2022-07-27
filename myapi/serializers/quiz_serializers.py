from datetime import datetime
from rest_framework import serializers
# from myapi.models import Quiz, Answer
from myapi.serializers.question_serializers import QuestionSerializer
from django.db.models.manager import Manager
from serpyco import SchemaBuilder, Serializer, nested_field ,post_dump,post_load, pre_dump ,pre_load
from dataclasses import dataclass
from typing import Callable, List, Union , Optional 
from myapi.serializers.user_serializers import User 
from myapi.serializers.course_serializers import CourseId
from myapi.serializers.serial import ID , CreatedAt , Validator 
from serpyco import AbstractValidator
from serpyco.validator import ValidationError


@dataclass 
class ContentType:
    model : str
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
    content_type : ContentType
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

############################################
@dataclass(kw_only=True)
class QuestionBaseValid:
    title : str
    image : str 
    owner : Optional[Union[User,int,None]] = None
@dataclass
class YNQValid(QuestionBaseValid,Correct):
    pass

@dataclass
class GQValid(QuestionBaseValid,Correct):
    pass
    
@dataclass
class MCQValid(QuestionBaseValid,Correct):
    option1 : str
    option2 : str
    option3 : str
    option4 : str

@dataclass
class QuestionValid:
    content_type :Union[ContentType,int]
    point : int
    item : Union[GQValid,YNQValid,MCQValid]
    quiz : ID
    deleted : int = 0

    @pre_load
    def pre_loading(data:dict):
        return data

    @post_dump
    def post_dumpping(data):
        # data['content_type']['model'] = data['content_type']['model'].upper()
        return data
        
    def dict(self):
        json = self.__dict__.copy()
        for k,v in json.items():
            print(type(v))
            if isinstance(v,tuple(QuestionBaseValid.__subclasses__())):
                json[k] = v.__dict__
        return json

_QuestionSchema = SchemaBuilder(QuestionValid)

QuestionValidator = Validator(schema_builder=_QuestionSchema)
QuizSerial = Serializer(Quiz)
QuizDetailSerial = Serializer(QuizDetail)
AnswerSerial = Serializer(Answer)
QuestionSerial = Serializer(Question)
QuestionOutSerial = Serializer(Question,exclude=["owner"])
QuestionVSerial = Serializer(QuestionValid)
YNQSerial = Serializer(YNQ)
GQSerial = Serializer(GQ)
MCQSerial = Serializer(MCQ)
