from django.db import models


class BaseItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.IntegerField(default=0)
    text = models.TextField(blank=False)
    image = models.ImageField()
    class Meta:
        abstract = True

class MSQ(BaseItem):
    choose = models.JSONField()
    correct = models.TextField(blank=False)


class YNQ(BaseItem):
    CHOICES = (("T","True"),("T","False"))

    correct = models.CharField(max_length=1,choices=CHOICES)

class GQ(BaseItem):
    answer = models.TextField(blank=False)

