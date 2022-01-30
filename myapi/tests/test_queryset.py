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
    
    a = AnswerCorrectFactory(user=u)
    a2 = AnswerCorrectFactory(user=u)
    p = User.objects.get_points(uid=u.id)
    print(p)
    assert p['points'] == 20

@pytest.mark.django_db
def test_correct_answer():
    a = AnswerCorrectFactory(point=9)
    q = Question.objects.all()[0].correct_answer
    print(q)
    print(a.user_answer)
    assert q == a.user_answer

@pytest.mark.django_db
def test_answer_factory_inherentence():
    total_point = 0
    a = AnswerCorrectFactory()
    total_point += a.point
    a2 = AnswerFactory(user=a.user)
    total_point += a2.point
    p = a.user.points
    assert p ==  total_point

