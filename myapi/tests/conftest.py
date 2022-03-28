import pytest
from rest_framework.test import APIClient
from myapi.tests.factories import *
import inspect
import random
import importlib


def pytest_runtest_setup(item):
    print("Hook Anounce", item)


@pytest.fixture
def API():
    return APIClient()


@pytest.fixture
def SUPER_LOGIN(API):
    u = UserFactory.create(username="login22", is_staff=True)
    API.force_authenticate(user=u)
    yield


@pytest.mark.django_db
@pytest.fixture
def user_login(request, API):
    u = UserFactory.create(username="login22", is_staff=request.param)
    API.force_authenticate(user=u)
    return API, request.param


@pytest.mark.django_db
@pytest.fixture
def CREATE_QUESTION(request):
    # print(request.getfixturevalue)
    print(request.node.function.__name__)
    # print(inspect.getfullargspec(request.node.function))
    question = ""
    x = request.getfixturevalue("r")
    for i in BaseQuestionFactory.__subclasses__():
        if x in i.__name__:
            question = i.create()
    return question


@pytest.mark.django_db
@pytest.fixture
def EXPORT_HTML(API, request):
    yield
    q = API.get("http://testserver/silk/", format="html")
    profile = API.get("/silk/profiling/", format="html")
    r = random.randint(1, 10)
    print(r)
    name = str(request.node.function.__name__) + str(r)
    name2 = str(request.node.function.__name__) + str("profile")
    f = open(f"{name}.html", "wb")
    f.write(q.content)
    f.close()
    f2 = open(f"{name2}.html", "wb")
    f2.write(profile.content)
    f2.close()
