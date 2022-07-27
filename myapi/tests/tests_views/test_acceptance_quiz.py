import pytest
from myapi.tests.factories import *
from django.db import connection
from django.test.utils import CaptureQueriesContext
from myapi.models2 import Question ,MCQ
from myapi.serializers.quiz_serializers import \
    _QuestionSchema , QuestionSerial , QuestionVSerial
    
@pytest.mark.service
@pytest.mark.question
def test_question_create_serializer():
    data= {
        "content_type":{"model":"GQ"},
        "quiz":{"id":1},
        "point":10,
        "fady":"Asdasd",
        "item":{
            "image":"Asdasd",
            "title":"a Title",
            "correct_answer":"Adasd"
        }
    }
    a = QuestionVSerial.load(data,validate=True)
    r = QuestionVSerial.dump(a,validate=True)
    print(r)
    print(a.point)
    print(a.dict())
    assert True == True


@pytest.mark.service
@pytest.mark.question
@pytest.mark.django_db
def test_question_delete_api(API):
    u = MCQFactory.create()
    
    quiz = QuizFactory.create()
    question = QuestionFactory.create(quiz=quiz,item=u)
    API.force_authenticate(user=quiz.course.owner)
    req = API.delete(f"/course/{quiz.course.id}/quiz/{quiz.id}/question/{question.id}/")
    print(req.data)
    question_check = Question.objects.count()
    mcq_check = MCQ.objects.count()
    assert mcq_check == 0
    assert question_check == 0
    assert req.status_code == 204
    
def _create_api(API):
    user = UserFactory.create(is_staff=1)
    course = CourseFactory.create(owner=user)
    quiz = QuizFactory.create(owner=user,course=course)
    API.force_authenticate(user=user)
    return API , user , course , quiz

@pytest.mark.question
@pytest.mark.service
@pytest.mark.django_db
def test_question_create_valid_api(API):
    API , user , course, quiz = _create_api(API)

    data= {
        "content_type":{"model":"GQ"},
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

    request = API.post(f"/course/{course.id}/quiz/{quiz.id}/question/",data=data,format="json")
    assert request.status_code == 201

@pytest.mark.service
@pytest.mark.question
@pytest.mark.django_db
def test_question_create_invalid_api(API):
    API , user , course, quiz = _create_api(API)


    data= {
        "content_type":{"model":"GQ"},
        "type2":"GQ2",
        "quiz":{"idx":quiz.id}, # wrong id not idx
        "point":"10", # wrong should be int
        "fady":"Asdasd",
        "item":{
            "image":"Asdasd",
            "title":"a Title",
            "correct_answer":"Adasd"
        }
    }

    request = API.post(f"/course/{course.id}/quiz/{quiz.id}/question/",data=data,format="json")
    assert request.status_code == 400
    
@pytest.mark.service
@pytest.mark.question
@pytest.mark.django_db
def test_question_list_api(API):
    user = UserFactory.create(is_staff=1)
    course = CourseFactory.create()
    quiz = QuizFactory.create(owner=user,course=course)
    mcq = MCQFactory.create()
    question = QuestionFactory.create(item=mcq,quiz=quiz)
    print(user.id)
    API.force_authenticate(user=course.owner)
    request = API.get(f"/course/{course.id}/quiz/{quiz.id}/question/",format="json")
    assert request.status_code == 200



@pytest.mark.service
@pytest.mark.question
@pytest.mark.django_db
def test_question_get_api(API):
    user = UserFactory.create(is_staff=1)
    course = CourseFactory.create()
    quiz = QuizFactory.create(owner=user,course=course)
    mcq = MCQFactory.create()
    question = QuestionFactory.create(item=mcq,quiz=quiz)
    print(user.id)
    API.force_authenticate(user=course.owner)
    request = API.get(f"/course/{course.id}/quiz/{quiz.id}/question/{question.id}/"\
        ,format="json")
    assert request.status_code == 200

# @pytest.mark.django_db
# def test_quiz_submit_answer(API, EXPORT_HTML):
    # nums = 6
    # u = UserFactory.create()
    # mcq = MCQFactory.create()
    # question = QuestionFactory.create(item=mcq)
    # course = Courses.objects.first()
    # u.courses.add(course)
    # u.save()
# 
    # API.force_authenticate(user=u)
    # question_quiz_id = question.quiz.id
    # question_answer= question.item.correct_answer
    # question_id = question.id
# 
    # with CaptureQueriesContext(connection) as ctx :
        # req = API.post(
            # f"/quiz/{question_quiz_id}/submit-answer/",
            # data=[
                # {"id": question_id, "user_answer": question_answer},
            # ],
            # format="json",
        # )
    # x = ctx.captured_queries
    # print("Length of queries = ", len(x))

    # assert req.status_code == 201
    # print(req.headers)
    # a = Answer.objects.get(user=u)
    # assert a.point == question.point
    # assert u.courses.count() == 1
# 
    # users = User.objects.all().count()
    # assert nums == users
# 