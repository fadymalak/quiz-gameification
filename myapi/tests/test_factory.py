
from attr import Factory
from myapi.models import Answer, Question, Quiz, User,Courses
import pytest
from .factories import *

pytestmark  = pytest.mark.factory

@pytest.mark.django_db
@pytest.mark.factory 
def test_factory_user():
    x = UserFactory.create_batch(3)
    print(type(x))
    assert 3 == len(x)

@pytest.mark.django_db
def test_factory_user_course():
    nums = 3
    u = UserFactory.create_batch(nums)
    course = CourseFactory.create(users=u,owner__first_name="aaa")
    owner = course.owner.first_name
    print(owner)
    assert nums == len(course.users.all())
    assert nums == len(u)

@pytest.mark.django_db
def test_factory_questions():
    nums = 4
    #create 3 Users by Quiz  + owner User 
    question = QuestionFactory.create()
    users = User.objects.all().count()
    assert nums == users
    print(question.title)
    assert True

@pytest.mark.django_db
def test_factory_quiz():
    quiz = QuizFactory.create()
    query = Quiz.objects.count()
    assert query == 1

@pytest.mark.django_db
def test_question_answer():
    question = QuestionFactory.create()
    usx = question.quiz.users.all()[0]
    Answer = AnswerFactory.create(point=0,user=usx,question=question,user_answer=question.correct_answer)
    assert Answer.user_answer == question.correct_answer
    