from django.db import models
from django.db.models import Count , F,Sum

class QuizQuerySet(models.QuerySet):
    def get_questions(self):
        return self.questions

    def get_quiz_total_points(self,title):
        #TODO Not Work Need Check Scope of QuerySet
        return self.get(title=title).questions.\
            aggregate(total_point=Sum(F("point")))

    def get_questions(self,title):
        return self.get(title=title).questions