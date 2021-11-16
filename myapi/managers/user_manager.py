from django.db import models
from ..querysets.user_queryset import UserQuerySet

class UserManager(models.Manager):
    def get_queryset(self):
        print(self._db)
        return UserQuerySet(model=self.model,using=self._db)

    def get_points(self):
        return self.get_queryset().get_points()

    def get_classes(self):
        return self.get_queryset().get_classes()
    
    def full_name(self):
        return self.get_queryset().full_name()