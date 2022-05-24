import pytest
from myapi.tests.factories import *
from django.db import connection
from django.test.utils import CaptureQueriesContext

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
