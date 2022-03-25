from django.utils.functional import cached_property
from django.db import models
from django.db.models.base import Model
import datetime
from django.db.models import Count , F , Sum
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import quiz_manager,user_manager,class_manager
from .querysets import quiz_queryset,course_queryset , user_queryset
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from .models2 import Question

class User(AbstractUser):
    
    id = models.AutoField(db_index=True,primary_key=True,serialize=True)
    username = models.CharField(max_length=25,unique=True,null=False)
    last_name = models.CharField(max_length=25,validators=[MinLengthValidator(limit_value=3)])
    first_name = models.CharField(max_length=25,validators=[MinLengthValidator(limit_value=3)])
    bio = models.CharField(max_length=50)
    picture = models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField("Courses",related_name="users")
    private = models.BooleanField(default=0)


    objects = user_manager.CustomUserManager()
    @property
    def full_name(self):
        return str(self.first_name+" "+self.last_name)
    
    @cached_property
    def points(self):
        return self.anwsers.filter(user=self.id).aggregate(points=Sum("point"))['points']

    def __str__(self):
        return self.first_name + " " + self.last_name
        
    # def save(self, *args,**kwargs):
        # if len(self.first_name) <= 2 or  len(self.last_name) <= 2:
            # raise ValidationError("Error First Name & Last Name length should be > 2")
        # super(User,self).save(*args,**kwargs)

class Courses(models.Model):
    id = models.AutoField(db_index=True,
                            primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=25)

    owner = models.ForeignKey(User,
                            related_name="course",
                            on_delete=models.CASCADE)

    objects = course_queryset.CourseQuerySet.as_manager()

    def get_quizs(self,next=5):
        return self.quizs.all().order_by("-created_at")[:next]
    
    @property
    def oname(self):
        '''
        self.owner.name
        '''
        return self.owner.first_name + " " + self.owner.last_name

    def __str__(self):
        return self.name +" -> "+self.owner.first_name

class Quiz(models.Model):
    id = models.AutoField(db_index=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    end_at = models.DateTimeField(
                                # default=\
                                # lambda n:datetime.datetime.now()+datetime.timedelta(days=7)
                                )
    users = models.ManyToManyField(User,related_name="quizs")
    # total_point = models.PositiveIntegerField()
    course = models.ForeignKey(Courses,related_name="quizs",on_delete=models.CASCADE)
    
    objects = quiz_queryset.QuizQuerySet.as_manager()


    def save(self,*args,**kwargs):
        self.end_at = datetime.datetime.now()+datetime.timedelta(days=7)
        return super(Quiz,self).save(*args,**kwargs)

    def get_points(self):
        return self.questions.aggregate(total_point=Sum(F("item__point")))
    
# class Question(models.Model):
    # id = models.AutoField(db_index=True,primary_key=True)
    # created_at = models.DateTimeField(auto_now_add=True)
# 
    # title = models.CharField(max_length=150)
    # point = models.IntegerField()
    # option1= models.CharField(max_length=150)
    # option2= models.CharField(max_length=150)
    # option3= models.CharField(max_length=150)
    # option4= models.CharField(max_length=150)
    # correct_answer = models.IntegerField()
    # quiz = models.ForeignKey(Quiz,related_name="questions",on_delete=models.CASCADE)
# 
class Answer(models.Model):
    STATUS_CHOICES = (("PENDING","PENDING"),("COMPLETED","COMPLETED"))
    id = models.AutoField(db_index=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField()
    user = models.ForeignKey(User,related_name="anwsers",on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question,related_name="anwsers",on_delete=models.DO_NOTHING)
    user_answer = models.TextField(default="")
    status = models.TextField(null=False,default="COMPLETED",choices=STATUS_CHOICES)
