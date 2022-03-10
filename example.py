print("hell1o")
from h11 import Data
from myapi.models2 import *
import random
from myapi.serializers.question_serializers import *
from myapi.tests.factories import UserFactory ,QuizFactory
qu = QuizFactory.create()
qu2 = QuizFactory.create()
u = UserFactory.create(id = random.randint(1,999999))
print(u.id)
x = YNQ(correct_answer="T",title="Did you Buy a car ?",owner=u)
x2 = GQ(correct_answer="ADASDASD",title="HHHHHHH",owner=u)
x.save()
q = Question(quiz=qu,item=x)

q2 = Question(quiz=qu2,item=x2)
q.save()
# q2.save()
print("-> ", str(isinstance(q.item,YNQ)))
s = QuestionSerializer(instance=q)
s2 = QuestionSerializer(instance=q2)
print( u.__dict__.items())
# print(User2( v for k,v in u.__dict__.items()))
# for key,value in dict.items():
    # setattr(self,key,value)
print(s2.data)
print(s.data)
# print(User3.dump(User2(username=u.username,id=u.id,private=u.private)))
print("hello")

# it