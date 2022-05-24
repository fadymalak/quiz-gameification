from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey , GenericRelation
from django.contrib.contenttypes.models import ContentType
from .models import *


class BaseItem(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    title = models.TextField(blank=False)
    image = models.URLField(null=True)
    owner = models.ForeignKey(
        "User", related_name="%(class)ss", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()

        return super(BaseItem, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Question(models.Model):
    quiz = models.ForeignKey("Quiz", related_name="questions", on_delete=models.CASCADE)
    deleted = models.IntegerField(default=0)
    qid = models.PositiveBigIntegerField(auto_created=True)
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={"model__in": ("mcq", "gq", "ynq")},
        on_delete=models.CASCADE,
    )
    point = models.PositiveIntegerField(default=1)
    item = GenericForeignKey("content_type", "qid")


class MCQ(BaseItem):
    option1 = models.CharField(max_length=150)
    option2 = models.CharField(max_length=150)
    option3 = models.CharField(max_length=150)
    option4 = models.CharField(max_length=150)
    correct_answer = models.TextField(blank=False)


class YNQ(BaseItem):
    CHOICES = (("T", "True"), ("F", "False"))
    correct_answer = models.CharField(max_length=3, choices=CHOICES)


class GQ(BaseItem):
    correct_answer = models.TextField(blank=False)


