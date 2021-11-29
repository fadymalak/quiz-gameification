from django.db import models
from django.db.models.base import Model
import datetime
from django.db.models import Count , F , Sum
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import quiz_manager,user_manager,class_manager
from .querysets import quiz_queryset,course_queryset
from django.utils import timezone
# class BasicModel(models.Model):
#     id = models.IntegerField(db_index=True,primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class meta:
#         abstract = True

class User(AbstractUser):
    id = models.IntegerField(db_index=True,primary_key=True)
    username = models.CharField(max_length=15,unique=True,null=False)
    last_name = models.CharField(max_length=15)
    first_name = models.CharField(max_length=15)
    bio = models.CharField(max_length=50)
    picture = models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField("Courses",related_name="users")

    # objects= user_manager.UserManager()
    def full_name(self):
        return str(self.first_name+" "+self.last_name)
    
    def get_courses(self):
        return self.courses.all()
    
class Courses(models.Model):
    id = models.IntegerField(db_index=True,
                            primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=25)

    owner = models.ForeignKey(User,
                            related_name="course",
                            on_delete=models.CASCADE)

    objects = course_queryset.CourseQuerySet.as_manager()

    
    def get_quizs(self,next=5):
        return self.quizs.all().order_by("-created_at")[:next]

class Quiz(models.Model):
    id = models.IntegerField(db_index=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    end_at = models.DateTimeField(
                                default=\
                                datetime.datetime.now()+datetime.timedelta(days=7)
                                )
    users = models.ManyToManyField(User,related_name="quizs")
    # total_point = models.PositiveIntegerField()
    course = models.ForeignKey(Courses,related_name="quizs",on_delete=models.CASCADE)

    objects = quiz_queryset.QuizQuerySet.as_manager()

    def get_points(self):
        return self.questions.aggregate(total_point=Sum(F("point")))
    
class Question(models.Model):
    id = models.IntegerField(db_index=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=150)
    point = models.IntegerField()
    option1= models.CharField(max_length=150)
    option2= models.CharField(max_length=150)
    option3= models.CharField(max_length=150)
    option4= models.CharField(max_length=150)
    correct_answer = models.IntegerField()
    quiz = models.ForeignKey(Quiz,related_name="questions",on_delete=models.CASCADE)

class Answer(models.Model):
    id = models.IntegerField(db_index=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField()
    user = models.ForeignKey(User,related_name="anwsers",on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question,related_name="anwsers",on_delete=models.DO_NOTHING)
    user_answer = models.IntegerField()

