from django.test import TestCase
from myapi.tests.factories import *
# Create your tests here.
from badges.models import *
import pytest
import datetime

@pytest.mark.django_db
@pytest.mark.not_implemented
@pytest.mark.rule
def test_create_rule(API):
    user = UserFactory.create(is_staff=1)
    ach = Achievement.objects.create(name="Achieve 1",owner=user)
    ach_level = AchievementLevel.objects.create(owner=user,name="Level1",image="/img.png",achievement=ach)
    API.force_authenticate(user=user)
    req = API.post("/achievement/1/rules/",data={
        'achievement_level':ach_level.id,
        'formula':'adasda',
        'interval':datetime.timedelta(days=1,seconds=5),
        'evalution_type':'weekly',
        'variable':{"name":"var 1"}
    },format="json")
    print(req.content)
    print(req.json())
    assert req.status_code == 201

