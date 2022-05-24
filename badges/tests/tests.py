from django.test import TestCase
from myapi.tests.factories import *
# Create your tests here.
from badges.models import *
import pytest
import datetime

@pytest.mark.django_db
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


@pytest.mark.django_db
def test_create_achievement(API):
    user = UserFactory.create(is_staff=1)
    print(user.id)
    data = {
        'achievement':{"name":"hello"},
        'name':'hello Level 1',
        

    }

    API.force_authenticate(user=user)
    req = API.post("/achievement/",data,format="json")
    data2 = data
    data2['parent'] = req.json()['id']
    req2 = API.post("/achievement/",data=data2,format="json")
    print(req.json())
    print("2-> ",req2.json())
    assert req2.status_code == 201
    assert req.status_code == 201