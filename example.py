print("hell1o")
# from h11 import Data

import os
import sys
import django


sys.path.append("quiz_gameification")
os.environ["DJANGO_SETTINGS_MODULE"] = "quiz_gameification.settings"
django.setup()
print("hello")
from myapi.models2 import *
from myapi.models import *
import random
from django.db.models import Prefetch
from myapi.serializers.quiz_serializers import *
from myapi.serializers.question_serializers import *
from myapi.tests.factories import QuestionFactory, UserFactory, QuizFactory, YNQFactory

print("Count Before: ", User.objects.all().count())

# QuestionFactory.create(item=YNQ.objects.filter(id=3).all()[0])
x = (
    Quiz.objects.filter(id=3)
    .prefetch_related(
        Prefetch(
            "questions",
            queryset=Question.objects.filter(ynq_related__deleted=1),
            to_attr="filter_questions",
        )
    )
    .all()
)
# w =YNQ.objects.all()[0].question.all()[0].qid
w = ""
instance = QuizDetailSerializer(instance=x)
print(instance.data)
print(User.objects.all().count())
x = 0


class Foo(object):
    def __str__(self):
        return "Hello From Foo"


if __name__ == "__main__":
    exit()
    print("Hello2")
    from myapi.models2 import *
    import random
    from myapi.serializers.question_serializers import *
    from myapi.tests.factories import UserFactory, QuizFactory

    print(User.objects.all().count())
    x = UserFactory.create(username="fadymalakawad")
    print(User.objects.all().count())
    exit()
    qu = QuizFactory.create()
    qu2 = QuizFactory.create()
    u = UserFactory.build(id=random.randint(1, 999999))
    print(u.id)
    x = YNQ(correct_answer="T", title="Did you Buy a car ?", owner=u)
    x2 = GQ(correct_answer="ADASDASD", title="HHHHHHH", owner=u)
    # x.save()
    q = Question(quiz=qu, item=x)

    q2 = Question(quiz=qu2, item=x2)
    # q.save()
    # q2.save()
    print("-> ", str(isinstance(q.item, YNQ)))
    s = QuestionSerializer(instance=q)
    s2 = QuestionSerializer(instance=q2)
    print(u.__dict__.items())
    # print(User2( v for k,v in u.__dict__.items()))
    # for key,value in dict.items():
    # setattr(self,key,value)
    print(s2.data)
    print(s.data)
    # print(User3.dump(User2(username=u.username,id=u.id,private=u.private)))
    print("hello")

    # it
