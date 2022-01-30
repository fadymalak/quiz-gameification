import pytest
from rest_framework.test import APIClient
from .factories import UserFactory
def pytest_runtest_setup(item):
    print("Hook Anounce",item)

@pytest.fixture
def API():
    return APIClient()

@pytest.fixture
def SUPER_LOGIN(API):
    u = UserFactory.create(username="login22",is_staff=True)
    API.force_authenticate(user=u)
    yield


@pytest.mark.django_db
@pytest.fixture
def user_login(request,API):
    u = UserFactory.create(username="login22",is_staff=request.param)
    API.force_authenticate(user=u)
    return API , request.param

