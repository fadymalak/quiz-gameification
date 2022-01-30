from django.db import models
from django.db.models.base import Model
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.
class BasicModel(models.Model):
    # id = models.IntegerField(db_index=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    class meta:
        abstract = True


class Course(BasicModel):
    name = models.CharField(max_length=25)
    owner = models.ForeignKey("Users",on_delete=models.CASCADE)    

class Users(AbstractUser,BasicModel):
    courses = models.ManyToManyField(Course,related_name="users")
    

# Create your models here.
class Qu(BasicModel):
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(Users,on_delete=models.CASCADE)
    end_at = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=7))
    userss = models.ManyToManyField(Users,related_name="quizs")
    # total_point = models.PositiveIntegerField()
    course = models.ForeignKey(Course,related_name="quizs",on_delete=models.CASCADE)
    
class Question(BasicModel):
    title = models.CharField(max_length=150)
    point = models.IntegerField()
    option1= models.CharField(max_length=150)
    option2= models.CharField(max_length=150)
    option3= models.CharField(max_length=150)
    option4= models.CharField(max_length=150)
    correct_answer = models.IntegerField()
    qu = models.ForeignKey(Qu,related_name="questions",on_delete=models.CASCADE)


class Answer(BasicModel):
    usera = models.ForeignKey(Users,related_name="anwsers",on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question,on_delete=models.DO_NOTHING)
    user_answer = models.IntegerField()

