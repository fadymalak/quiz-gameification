from django.test import TestCase
from ..models import *
from ..serializers.user_serializers import UserSerializer


class UserTestCase(TestCase):
    
    def setUp(self) -> None:
        self.POINT = 10
        User.objects.create(first_name="fady",
        last_name="malak",
        password="123567",
        username="fadymalak2",
        )
        User.objects.create(first_name="Professor",
        last_name="Test1",
        password="123567",username="proftest",
        )

        user = User.objects.get(first_name="fady")
        prof = User.objects.get(first_name="Professor")
        Courses.objects.create(name="Math",owner=prof)
        course = Courses.objects.get(name="Math")
        Quiz.objects.create(title="First Math Quiz",
        owner=prof, course=course)
        quiz = Quiz.objects.get(title__startswith="First")
        quiz.users.add(user)
        Question.objects.create(title="Whats is your name ?",
        point=self.POINT,
        option1="fady",
        option2="fady2",
        option3="fady3",
        option4="fady4",
        correct_answer=1,
        quiz=quiz
        )
        Question.objects.create(title="Whats is your name 2?",
        point=self.POINT,
        option1="fady1",
        option2="fady24",
        option3="fady35",
        option4="fady46",
        correct_answer=1,
        quiz=quiz
        )
        Question.objects.create(title="Whats is your name 3?",
        point=self.POINT,
        option1="fady1",
        option2="fady24",
        option3="fady35",
        option4="fady46",
        correct_answer=1,
        quiz=quiz
        )
        self.MAX_POINT = 30

    def test_user_point(self):
        pass

    def test_user_courses(self):
        pass
    
    def test_fullname(self):
        user = User.objects.get(username="fadymalak2")
        check_user = user.full_name()
        user_data = UserSerializer(user).data
        return self.assertEqual(user_data['name'],check_user)

