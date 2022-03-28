from django.db import models
from django.contrib.auth.models import BaseUserManager, UserManager
from ..querysets.user_queryset import UserQuerySet


class CustomUserManager(UserManager, models.Manager):
    def get_queryset(self):
        return UserQuerySet(model=self.model, using=self._db)

    def get_points(self, uid):
        return self.get_queryset().get_points(uid=uid)

    def get_classes(self):
        return self.get_queryset().get_classes()

    def professors(self):
        return self.get_queryset().professors()
