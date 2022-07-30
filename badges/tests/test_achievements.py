from myapi.tests.factories import UserFactory
import pytest
from myapi.tests.factories import UserFactory
from badges.services.achievement import AchievementLevelService , AchievementService
from badges.factories import AchievementFactory , AchievementLevelFactory

@pytest.mark.django_db
@pytest.mark.curr
@pytest.mark.achievement
def test_achievement_service():
    user = UserFactory.create()
    data = {"name":"Achievement Killer","owner":user}
    ach = AchievementService.create(name=data['name'],owner=data['owner'])[0]
    assert ach.name == data['name']
    assert ach.owner.username == user.username


@pytest.mark.django_db
@pytest.mark.curr
@pytest.mark.achievement
def test_retrieve_achivement(API):
    user = UserFactory.create(is_staff=1)
    achievement = AchievementFactory.create(owner=user)

    API.force_authenticate(user=user)
    req = API.get(f"/achievement/{achievement.id}/")
    assert req.status_code == 200
    assert achievement.name == req.data['name']


@pytest.mark.django_db
@pytest.mark.curr
@pytest.mark.achievement
def test_create_achievement(API):
    user = UserFactory.create(is_staff=1)
    print(user.id)
    data = {
        'name':'hello Level 1',
    }
    API.force_authenticate(user=user)
    req = API.post("/achievement/",data,format="json")
    assert req.status_code == 201


@pytest.mark.django_db
@pytest.mark.curr
@pytest.mark.achievement
def test_update_achievement(API):
    user = UserFactory.create(is_staff=1)
    achievement = AchievementFactory.create(owner=user)

    data = {
        'name':'hello Level 1',
    }
    API.force_authenticate(user=user)
    req = API.patch(f"/achievement/{achievement.id}/",format="json",data=data)
    assert req.status_code == 200
    assert achievement.name != req.data['name']


@pytest.mark.django_db
@pytest.mark.achievement
@pytest.mark.curr
def test_create_achievement_level(API):
    user = UserFactory.create(is_staff=1)
    achievement = AchievementFactory.create(owner=user)
    API.force_authenticate(user=user)
    data = {
        'name':'hello Level 1',
    }
    req = API.post(f"/achievement/{achievement.id}/level/",format="json",data=data)
    assert req.status_code == 201

@pytest.mark.django_db
@pytest.mark.achievement
@pytest.mark.curr
def test_get_achievement_level(API):
    user = UserFactory.create(is_staff=1)
    achievement = AchievementFactory.create(owner=user)
    level = AchievementLevelFactory.create(achievement=achievement)
    API.force_authenticate(user=user)
    req = API.get(f"/achievement/{achievement.id}/level/{level.id}/")
    assert req.status_code == 200
    assert req.data['name'] == level.name


@pytest.mark.django_db
@pytest.mark.achievement
@pytest.mark.curr
def test_get_achievement_level(API):
    user = UserFactory.create(is_staff=1)
    achievement = AchievementFactory.create(owner=user)
    level = AchievementLevelFactory.create(achievement=achievement)
    level2 = AchievementLevelFactory.create(achievement=achievement)
    API.force_authenticate(user=user)
    data = {"parent":level2.id}
    req = API.patch(f"/achievement/{achievement.id}/level/{level.id}/",format="json",data=data)
    assert req.status_code == 200
    assert req.data['name'] == level.name