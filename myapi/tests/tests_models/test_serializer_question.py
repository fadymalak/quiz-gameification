from functools import partial
from myapi.serializers.question_serializers import *
import pytest
from myapi.tests.factories import *
from myapi.usecase.quiz import question_update
from myapi.serializers.quiz_serializers import QuestionSerial
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
@pytest.mark.parametrize("r", ["MCQ", "GQ", "YNQ"])
def test_question_deserializer_create(r, CREATE_QUESTION):
    """POST:create get json data to create instance"""
    serial = ""
    for i in BaseItemSerializer.__subclasses__():
        if r.lower() in i.__name__.lower():
            serial = i(CREATE_QUESTION)

    data = serial.data

    data["type"] = r.lower()
    data["owner"] = CREATE_QUESTION.owner.username
    user = UserFactory.create()
    quiz = QuizFactory.create()

    question = {"item": data, "quiz": quiz.id, "point": 20}
    serial2 = QuestionSerializer(data=question)
    serial2.is_valid()
    serial2.save()
    que = Question.objects.all()[0]
    print(type(que.deleted))
    result = serial2.data
    print(result)
    assert result["item"]["owner"] == CREATE_QUESTION.owner.username
    # TODO check api delete:int   type str or int
    assert int(result["deleted"]) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("r", ["MCQ", "GQ", "YNQ"])
def test_serializer_question_fetch(r, CREATE_QUESTION):
    """GET:reterive create item/fetch item then serialize it"""
    question_item = CREATE_QUESTION
    quiz = QuizFactory.create()
    question = Question(item=question_item, quiz=quiz)
    question.save()
    serial = QuestionSerializer(question)
    result = serial.data
    assert result["item"]["owner"] == question_item.owner.username


@pytest.mark.django_db
@pytest.mark.not_implemented
@pytest.mark.parametrize("r", ["MCQ", "GQ", "YNQ"])
def test_serializer_question_full_update(r, CREATE_QUESTION):
    """PUT/UPDATE  NEED UPDATE & partial UPDATE"""
    for i in BaseItemSerializer.__subclasses__():
        if r.lower() in i.__name__.lower():
            serial = i(CREATE_QUESTION)

    data = serial.data
    data["type"] = r.lower()
    data["owner"] = CREATE_QUESTION.owner.username
    user = UserFactory.create()
    quiz = QuizFactory.create()
    question = Question(item=CREATE_QUESTION, quiz=quiz, point=0)
    question.save()
    print(question.point)
    data["title"] = "Questionssss"
    question_data = {"id": question.id, "quiz": quiz.id, "point": 20}
    question_serial = QuestionSerializer(question, data=question_data, partial=True)
    question_serial.is_valid()
    question_serial.save()
    print(question_serial.data)
    assert 1 == 1


@pytest.mark.django_db
@pytest.mark.parametrize("r", ["MCQ", "GQ", "YNQ"])
def test_question_update_partial(r, CREATE_QUESTION):
    """PUT/UPDATE  NEED UPDATE & partial UPDATE"""
    for i in BaseItemSerializer.__subclasses__():
        if r.lower() in i.__name__.lower():
            serial = i(CREATE_QUESTION)
    data = serial.data
    data.pop("type")
    data.pop("owner")
    user = UserFactory.create()
    quiz = QuizFactory.create()
    question = Question(item=CREATE_QUESTION, quiz=quiz, point=0)
    question.save()
    print(question.point)
    data["title"] = "Questionssss"
    question_data = {"id": question.id,'content_type':{'model':r.lower()}, "item": data, "point": 20}

    print(question_data)
    obj = question_update(question_id=question.id,data=question_data)
    serial = QuestionSerial.dump(obj)
    print(serial)

    assert obj.item.title == data['title']
