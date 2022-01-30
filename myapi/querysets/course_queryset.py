

from django.db import models


class CourseQuerySet(models.QuerySet):
    def get_owner(self):
        return self.owner

    def get_users(self,name):
        return self.get(name=name).users

    def get_quizs(self):
        return self.quizs