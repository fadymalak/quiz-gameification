from django.db import models


class ClassManager(models.Manager):
    def get_owner(self):
        return self.owner

    def get_users(self):
        return self.users

    def get_quizs(self):
        return self.quizs