import pytest
from myapi.tests.factories import *
from django.db import connection
from django.test.utils import CaptureQueriesContext
from myapi.serializers.quiz_serializers import \
    NestValidator , _QuestionSchema , Question, QuestionSerial , QuestionVSerial
    
# @pytest.mark.service
def test_question_create_serializer():
    data= {
        "content_type":"GQ",
        "quiz":{"id":1},
        "point":10,
        "fady":"Asdasd",
        "item":{
            "image":"Asdasd",
            "title":"a Title",
            "correct_answer":"Adasd"
        }
    }
    # valid = NestValidator(_QuestionSchema).validate(data,nest=["item"])
    a = QuestionVSerial.load(data,validate=True)
    r = QuestionVSerial.dump(a,validate=True)
    print(r)
    print(a.point)
    print(a.dict())
    assert True == True

@pytest.mark.service
@pytest.mark.django_db
def test_question_create_db(API):
    u = MCQFactory.create()
    
    quiz = QuizFactory.create()
    question = QuestionFactory.create(quiz=quiz,item=u)
    print(QuestionVSerial.dump(question))
    assert 1 == 1


@pytest.mark.service
@pytest.mark.django_db
def test_question_create(API):
    user = UserFactory.create(is_staff=1)
    course = CourseFactory.create(owner=user)
    quiz = QuizFactory.create(owner=user,course=course)
    data= {
        "content_type":"GQ",
        "type2":"GQ2",
        "quiz":{"id":quiz.id},
        "point":10,
        "fady":"Asdasd",
        "item":{
            "image":"Asdasd",
            "title":"a Title",
            "correct_answer":"Adasd"
        }
    }
    print(user.id)
    API.force_authenticate(user=user)
    request = API.post(f"/course/{course.id}/quiz/{quiz.id}/question/",data=data,format="json")
    print(request.data)
    assert request.status_code == 201
@pytest.mark.django_db
def test_quiz_submit_answer(API, EXPORT_HTML):
    nums = 6
    u = UserFactory.create()
    mcq = MCQFactory.create()
    question = QuestionFactory.create(item=mcq)
    course = Courses.objects.first()
    u.courses.add(course)
    u.save()

    API.force_authenticate(user=u)
    question_quiz_id = question.quiz.id
    question_answer= question.item.correct_answer
    question_id = question.id

    with CaptureQueriesContext(connection) as ctx :
        req = API.post(
            f"/quiz/{question_quiz_id}/submit-answer/",
            data=[
                {"id": question_id, "user_answer": question_answer},
            ],
            format="json",
        )
    x = ctx.captured_queries
    print("Length of queries = ", len(x))
    # for i in x:
        # print( "--> ",i['sql'])

    assert req.status_code == 201
    print(req.headers)
    a = Answer.objects.get(user=u)
    assert a.point == question.point
    assert u.courses.count() == 1

    users = User.objects.all().count()
    assert nums == users
