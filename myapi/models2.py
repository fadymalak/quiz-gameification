from lib2to3.pytree import Base
from django.db import models 
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .models  import *

class BaseItem(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    deleted = models.IntegerField(default=0)
    title = models.TextField(blank=False)
    image = models.ImageField(default='')
    owner = models.ForeignKey("User",related_name="%(class)ss"
                        ,on_delete=models.CASCADE)
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.created_at = timezone.now()

        return super(BaseItem,self).save(*args,**kwargs)
    class Meta:
        abstract = True

class Question(models.Model):
    quiz = models.ForeignKey("Quiz",related_name="questions",on_delete=models.CASCADE)
    qid = models.PositiveBigIntegerField(auto_created=True)
    content_type = models.ForeignKey(ContentType,limit_choices_to=
                                    {'model__in':
                                    ('mcq','gq','ynq')
                                    }
                                    ,on_delete=models.CASCADE)
    item = GenericForeignKey('content_type','qid')

class MCQ(BaseItem):
    option1= models.CharField(max_length=150)
    option2= models.CharField(max_length=150)
    option3= models.CharField(max_length=150)
    option4= models.CharField(max_length=150)
    correct_answer = models.TextField(blank=False)


class YNQ(BaseItem):
    CHOICES = (("T","True"),("T","False"))
    correct_answer = models.CharField(max_length=1,choices=CHOICES)

class GQ(BaseItem):
    correct_answer = models.TextField(blank=False)


