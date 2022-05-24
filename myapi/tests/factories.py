from attr import Factory
import factory
from factory.helpers import post_generation
from ..models import Answer, Quiz, User, Courses  # ,Question
from ..models2 import GQ, YNQ, Question, MCQ
import pytest
from django.contrib.contenttypes.models import ContentType
import random
from .utils import update
import factory.fuzzy
import datetime
def rando():
    d = datetime.datetime.timestamp(datetime.datetime.now())
    d = int(d)
    r = random.randint(1,99)
    return int(str(d)+str(r)) +random.randint(1,100000)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # BUGFIX If id not provided object will return id None
    id = factory.Sequence(lambda _: rando())  # LazyAttribute(lambda _ :update('u'))
    username = factory.faker.Faker("user_name")
    last_name = factory.faker.Faker("first_name")
    first_name = factory.faker.Faker("first_name")


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Courses

    id = factory.Sequence(lambda _: rando())
    name = factory.Sequence(lambda o: "course Number %s" % o)
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return
        self.users.add(*extracted)


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    id = factory.LazyAttribute(lambda _: rando())
    title = factory.Sequence(lambda n: "Quiz %s" % n)
    owner = factory.SelfAttribute("course.owner")
    course = factory.SubFactory(CourseFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        # if no specified  create 3 Users
        if not extracted:
            create_users = UserFactory.create_batch(3)
            self.users.add(*create_users)
        else:
            self.users.add(*extracted)
        self.save()


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    id = factory.LazyAttribute(lambda _: rando())
    point = factory.fuzzy.FuzzyInteger(1, 50)
    quiz = factory.SubFactory(QuizFactory)
    deleted = 0
    qid = factory.SelfAttribute("item.id")
    content_type = factory.LazyAttribute(
        lambda c: ContentType.objects.get_for_model(c.item)
    )


class BaseQuestionFactory(factory.django.DjangoModelFactory):
    # deleted = 0  # fixed Value
    title = factory.Sequence(lambda n: "Question %s" % (n))
    image = "\\Users\\fady\\Desktop\\python projects\\quiz_gameification\\projects\\quiz_gameification\\1.png"  # fixed value
    owner = factory.SubFactory(UserFactory)

    class Meta:
        abstract = True


class GQFactory(BaseQuestionFactory):
    # item = factory.SubFactory(GQSub)
    # id = factory.Sequence(lambda n: int(n))
    correct_answer = factory.Sequence(lambda n: "GQ Answer: %s" % (n))

    class Meta:
        model = GQ

    def __str__(self):
        return "GQ"


class MCQFactory(BaseQuestionFactory):
    # item = factory.SubFactory(MCQSub)
    option1 = factory.Sequence(lambda n: "Answer %s" % n)
    option2 = factory.Sequence(lambda n: "Answer %s" % n)
    option3 = factory.Sequence(lambda n: "Answer %s" % n)
    option4 = factory.Sequence(lambda n: "Answer %s" % n)
    correct_answer = factory.fuzzy.FuzzyInteger(1, 4)
    # correct_answer = factory.Sequence(lambda n :"GQ Answer: %s"%(n))
    class Meta:
        model = MCQ


class YNQFactory(BaseQuestionFactory):
    # item = factory.SubFactory(YNQSub)
    correct_answer = factory.Sequence(lambda n: ["T", "F"][random.randint(0, 1)])

    class Meta:
        model = YNQ


class AnsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
        abstract = True

    id = factory.LazyAttribute(lambda _: rando())
    point = factory.LazyAttribute(lambda _: random.randint(0, 10))
    user = factory.SubFactory(UserFactory)
    user_answer = factory.fuzzy.FuzzyInteger(1, 4)
    question = factory.SubFactory(QuestionFactory)


class AnswerFactory(AnsFactory):
    pass


class AnswerCorrectFactory(AnsFactory):
    point = int(10)
    question = factory.SubFactory(
        QuestionFactory, correct_answer=factory.SelfAttribute("..item.user_answer")
    )
