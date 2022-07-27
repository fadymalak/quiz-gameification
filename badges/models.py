from functools import cached_property
from django.db import models
from myapi.models import User
from django.utils import timezone


# Create your models here.
class Achievement(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    @cached_property
    def owner_username(self):
        return self.owner.username
        
class AchievementLevel(models.Model):
    achievement = models.ForeignKey(Achievement,on_delete=models.CASCADE)
    parent = models.ForeignKey("self",null=True,on_delete=models.CASCADE)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.TextField()
    image = models.URLField(null=True)

class UserAchievement(models.Model):
    user = models.ForeignKey(User,related_name="achievements",on_delete=models.CASCADE)
    achievement_level = models.ForeignKey(AchievementLevel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Variable(models.Model):
    name = models.TextField()

class Rules(models.Model):
    achievement_level = models.ForeignKey(AchievementLevel,related_name="rules",on_delete=models.CASCADE)
    formula = models.TextField()
    interval = models.DurationField()
    evalution_type = models.CharField(max_length=10)
    variable = models.ForeignKey(Variable,related_name="rule",on_delete=models.CASCADE)
    group_key = models.IntegerField(null=True)

class VariableUser(models.Model):
    user = models.ForeignKey(User,related_name="variables",on_delete=models.CASCADE)
    variable = models.ForeignKey(Variable,on_delete=models.CASCADE)
    value = models.PositiveBigIntegerField()
    update_at = models.DateTimeField(auto_now=True)


class VariableUserDetials(models.Model):
    variable_user = models.ForeignKey(VariableUser,related_name="detials",on_delete=models.CASCADE)
    value = models.PositiveBigIntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now = True)

