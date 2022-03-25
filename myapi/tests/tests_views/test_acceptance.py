import pytest
from myapi.tests.factories import *


@pytest.mark.django_db
def test_quiz_submit_answer(API,EXPORT_HTML):
    nums = 6
    u = UserFactory.create()
    mcq = MCQFactory.create()
    question = QuestionFactory.create(item=mcq)
    course = Courses.objects.first()
    u.courses.add(course)
    u.save()
    API.force_authenticate(user=u)
    req = API.post(f"/quiz/{question.quiz.id}/submit-answer/",data=[{"id":question.id,
                            "user_answer":question.item.correct_answer},],
                            format='json')

    assert req.status_code == 201
    print(req.headers)
    a = Answer.objects.get(user=u)
    assert a.point == question.point
    assert u.courses.count() == 1
    
    users = User.objects.all().count()
    assert nums == users