
from django.db import models
from django.db.models import Count , F


class UserQuerySet(models.QuerySet):
    def professor(self):
        pass
    def get_points(self):
        return self.annotate(points=Count(F(self.anwsers.point)))

    def get_classes(self):
        return self.courses
    
