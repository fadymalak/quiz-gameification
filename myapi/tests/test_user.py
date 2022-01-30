from django.test import TestCase
from myapi.models import *
from myapi.serializers.user_serializers import UserSerializer
from .factories import *
import pytest

@pytest.mark.django_db
@pytest.mark.parametrize("n",[x for x in range(1,7)])
def test_user_name(n):#,check_name_type):
    x = UserFactory.create(id=n)
    assert type(x.first_name) == str
