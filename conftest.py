import pytest
from rest_framework.test import APIClient
from myapi.tests.factories import *
import inspect
import random
import importlib
from quiz_gameification import settings
from django.db import connections
import sqlite3
# def run_sql(sql):
    # conn = sqlite3.connect(database='test.sqlite',check_same_thread=False)
    # cur = conn.cursor()
    # cur.execute(sql)
    # conn.close()
# 
# TODO if i uncomment this function it will Use settings_test default
#now it use in-memory sqlite
# @pytest.fixture(scope='session')
# def django_db_setup():
    # '''Custom database configuration for Test'''
# 
    # yield
#     for connection in connections.all():
#         connection.close()
# # 
    # run_sql("select 'delete from ' || name from sqlite_master where type = 'table';")



def pytest_runtest_setup(item):
    print(f"Hook Anounce", item)


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
