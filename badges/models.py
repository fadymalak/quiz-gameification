from django.db import models
from myapi.models import User
# Create your models here.
class Rule(models.Model):
    CHOICES = [
        ("POINT","POINT"),
        ("NUMBER_OF_QUIZS","NUMBER_OF_QUIZS"),
        ("NUMBER_OF_CORRECT_QUESTION","NUMBER_OF_CORRECT_QUESTION"),
        ("ACTIVE","ACTIVE")]
    name = models.CharField(max_length=150)
    require_type = models.CharField(choices=CHOICES)
    require = models.IntegerField()

class Badge(models.Model):
    name  = models.CharField(max_length=150,null=False)
    image = models.ImageField(upload_to="upload/badges/")
    rules = models.ManyToManyField(Rule,related_name="badges") 
    created_at = models.DateTimeField(auto_now_add=True)
    enable  = models.IntegerField(default=1)
    users = models.ManyToManyField(User,related_name="badges")
