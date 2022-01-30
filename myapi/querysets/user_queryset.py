
from django.db import models
from django.db.models import Count , F , Sum


class UserQuerySet(models.QuerySet):
    def professors(self):
        return self.filter(is_staff=True)

    #Show Be Removed 'User' object has no attribute 'get_points'
    def get_points(self,uid):
        return self\
            .filter(id=uid)\
            .aggregate(points=Sum("anwsers__point"))

    def get_classes(self):
        return self.courses.all()
    
