import factory
from factory.helpers import post_generation
from ..models import Answer, Question, Quiz, User,Courses
import pytest
import random
from .utils import update
import factory.fuzzy
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # BUGFIX If id not provided object will return id None
    id = factory.Sequence(lambda n: int(n))#LazyAttribute(lambda _ :update('u'))
    username = factory.faker.Faker('user_name')
    last_name = factory.faker.Faker("name")
    first_name = factory.faker.Faker("name")
    
 
class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Courses
    id = factory.Sequence(lambda n: int(n))
    name= factory.Sequence(lambda o: "course Number %s"%o)
    owner = factory.SubFactory(UserFactory)
    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return
        self.users.add(*extracted)

class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Quiz
    id = factory.LazyAttribute(lambda _:update('gw'))
    title = factory.Sequence(lambda n : "Quiz %s"%n)
    owner = factory.SelfAttribute("course.owner")
    course = factory.SubFactory(CourseFactory)
    
    @factory.post_generation
    def users(self,create,extracted,**kwargs):
        if not create:
            return

        #if no specified  create 3 Users
        if not extracted :
            create_users = UserFactory.create_batch(3)
            self.users.add(*create_users)
        else:
            self.users.add(*extracted)
        self.save()

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
    id = factory.LazyAttribute(lambda _:update('gw'))
    title = factory.Sequence(lambda n:"Question %s"%(n))
    option1 = factory.Sequence(lambda n: "Answer %s"%n)
    option2 = factory.Sequence(lambda n: "Answer %s"%n)
    option3 = factory.Sequence(lambda n: "Answer %s"%n)
    option4 = factory.Sequence(lambda n: "Answer %s"%n)
    correct_answer = factory.fuzzy.FuzzyInteger(1,4)
    point = factory.fuzzy.FuzzyInteger(10,50)
    quiz = factory.SubFactory(QuizFactory)

class AnsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
        abstract =True
    id = factory.LazyAttribute(lambda _:update('gw'))
    point = factory.LazyAttribute(lambda _: random.randint(0,10))
    user = factory.SubFactory(UserFactory)
    user_answer = factory.fuzzy.FuzzyInteger(1,4)
    question = factory.SubFactory(QuestionFactory)

class AnswerFactory(AnsFactory):
    pass

class AnswerCorrectFactory(AnsFactory):
    point = int(10)
    question = factory.SubFactory(QuestionFactory,\
        correct_answer=factory.SelfAttribute('..user_answer'))
