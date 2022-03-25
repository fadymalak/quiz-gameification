from myapi.models import *
import pytest
from .factories import *

@pytest.mark.django_db
def test_user_query():
    u = UserFactory.create(is_staff=True)
    q = User.objects.professors().count()
    assert q == 1

@pytest.mark.django_db
def test_user_queryset_get_points():
    u = UserFactory.create()
    mcq = MCQFactory.create()
    q = QuestionFactory.create(item=mcq)
    a = AnswerCorrectFactory(user=u,question=q)
    a2 = AnswerCorrectFactory(user=u,question=q)
    p = User.objects.get_points(uid=u.id)
    assert p['points'] == 20

@pytest.mark.django_db
def test_correct_answer():
    mcq = MCQFactory.create()
    q = QuestionFactory.create(item=mcq)
    a = AnswerCorrectFactory(point=9,question=q,user_answer=mcq.correct_answer)
    q = Question.objects.all()[0].item.correct_answer
    print(q)
    print(a.user_answer)
    assert int(q) == a.user_answer

@pytest.mark.django_db
def test_answer_factory_inherentence():
    mcq = MCQFactory.create()
    q = QuestionFactory.create(item=mcq)
    total_point = 0
    a = AnswerCorrectFactory(question=q)
    total_point += a.point
    a2 = AnswerFactory(user=a.user,question=q)
    total_point += a2.point
    p = a.user.points
    assert p ==  total_point

