from rest_framework.test import APIClient
import pytest
from myapi.serializers.quiz_serializers import QuizDetailSerializer
from myapi.tests.utils import gen_quiz_data
from myapi.tests.factories import *
from django.test.utils import CaptureQueriesContext
from django.db import connection
import datetime
from rest_framework import status


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 201), (False, False, 403), (False, True, 403), (True, False, 403)],
)
def test_acceptance_CREATE_quiz_endpoint(API, teacher, own, result):
    u = UserFactory.create(is_staff=teacher)
    if own == False and teacher == True:
        """
        test if other teacher (not owner of course)
            can create quiz in courses not owing them
        """
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner=u1)
    else:
        c = CourseFactory.create(owner=u)

    API.force_authenticate(user=u)
    data = gen_quiz_data(
        title="Quiz%s" % (str(teacher)),
        owner=u.id,
        course=c.id,
        end_at=str(datetime.datetime.now()),
    )
    request = API.post("/quiz/", data=data)
    assert request.status_code == result


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 204), (False, False, 403), (False, True, 403), (True, False, 403)],
)
def test_acceptance_DELETE_quiz_endpoint(API, teacher, own, result):
    u = UserFactory.create(is_staff=teacher)
    if own == False and teacher == True:
        """
        test if other teacher (not owner of course)
            can :delete: quiz in courses not owing them
        """
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner=u1)
        quiz = QuizFactory.create(owner=u1, course=c)
    else:
        c = CourseFactory.create(owner=u)
        quiz = QuizFactory.create(owner=u, course=c)

    API.force_authenticate(user=u)
    before = Quiz.objects.filter(id=quiz.id).count()
    data = {"course": c.id}
    request = API.delete(f"/quiz/{quiz.id}/")
    after_result = Quiz.objects.filter(id=quiz.id).count()
    if result != 204:
        after = 1
    else:
        after = 0
    print(request.status_code)
    assert before == 1
    assert after_result == after
    assert request.status_code == result


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 200), (False, False, 403), (False, True, 403), (True, False, 403)],
)
def test_update_quiz_endpoint(API, teacher, own, result):
    u = UserFactory.create(is_staff=teacher)
    if own == False and teacher == True:
        """
        test if other teacher (not owner of course)
            can :delete: quiz in courses not owing them
        """
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner=u1)
        quiz = QuizFactory.create(owner=u1, course=c)
    else:
        c = CourseFactory.create(owner=u)
        quiz = QuizFactory.create(owner=u, course=c)

    API.force_authenticate(user=u)
    serial = QuizDetailSerializer(quiz)
    data = serial.data
    print(data)
    data["title"] = "QUIZOOOOO"
    request = API.patch(f"/quiz/{quiz.id}/", data=data, format="json")

    print(request.status_code)
    rdata = request.data
    print(rdata)
    print(request.content)
    if request.status_code == 200:
        assert data["title"] == rdata["title"]

    assert request.status_code == result


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.curr
# @pytest.mark.count_queries
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 201), (False, False, 403), (False, True, 403), (True, False, 403)],
)
def test_retreive_quiz_endpoint(API, teacher, own, result):
    user = UserFactory.create()
    API.force_authenticate(user=user)
    course = CourseFactory.create(owner=user)
    quiz = QuizFactory.create(course=course)
    question_item = MCQFactory.create()
    question_item2 = MCQFactory.create()
    question_item3 = GQFactory.create()
    question = QuestionFactory.create(item=question_item, quiz=quiz)
    question = QuestionFactory.create(item=question_item2, quiz=quiz)
    question = QuestionFactory.create(item=question_item3, quiz=quiz)
    # get all queries
    with CaptureQueriesContext(connection) as ctx:
        req = API.get(f"/quiz/{quiz.id}/")
    x = ctx.captured_queries
    print(f"[*] length : {len(x)}")
    for i in x:
        print("-> ", i["sql"])
    assert req.status_code == 200
    assert req.data["title"] == quiz.title
    assert len(req.data["questions"]) == 3


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 201), (False, False, 403), (False, True, 403), (True, False, 403)],
)
def test_list_quiz_endpoint(API, teacher, own, result):
    # TODO fetch only course quizs
    LENGTH = 4
    user = UserFactory.create()
    API.force_authenticate(user=user)
    course = CourseFactory.create(owner=user)
    quiz = QuizFactory.create_batch(LENGTH, course=course)
    req = API.get("/quiz/")

    assert LENGTH == len(req.data)
