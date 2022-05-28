from random import randint
import pytest
from myapi.tests.factories import UserFactory


@pytest.mark.user
#@pytest.mark.service
@pytest.mark.django_db
def test_create_vaild_user(API):
    data = {
        "username":"fadymalak",
        "password":"Fady.123",
        "first_name":"fady",
        "first_name":"malak",
        "private":0,
        "bio":"My name is Fady",
    }
    request = API.post("/user/",data=data,format="json")
    assert request.status_code == 201


@pytest.mark.user
#@pytest.mark.service
@pytest.mark.django_db
def test_create_invaild_user(API):
    data = {
        "username":"fadymalak",
        "password":"Fady.123",
        "first_name":"fady",
        "first_name":"malak",
        "private":0,
        "bio":"My name is Fady",
        'Wrong_object' :"eval"
    }
    request = API.post("/user/",data=data,format="json")
    assert request.status_code == 400


@pytest.mark.user
#@pytest.mark.service
@pytest.mark.django_db
def test_patch_vaild_user(API):
    user = UserFactory.create()
    data = {
        "bio":"My name is Fady",
    }
    API.force_authenticate(user=user)

    request = API.patch(f"/user/{user.id}/",data=data,format="json")
    assert request.status_code == 200
    assert request.data['bio'] == "My name is Fady"



@pytest.mark.user
#@pytest.mark.service
@pytest.mark.django_db
def test_patch_zinvaild_user(API):
    user = UserFactory.create()
    data = {

        "bio":"My name is Fady",
        'Wrong_object' :"eval"
    }
    API.force_authenticate(user=user)
    request = API.patch(f"/user/{user.id}/",data=data,format="json")
    assert request.status_code == 400

@pytest.mark.user
#@pytest.mark.service
@pytest.mark.django_db
def test_get_anonymous_user(API):
    user = UserFactory.create()
    request = API.get(f"/user/{user.id}/")
    assert request.status_code == 403
    

@pytest.mark.user
#@pytest.mark.service
@pytest.mark.django_db
def test_get_loggedin_user(API):
    user = UserFactory.create()
    user2  = UserFactory.create()
    API.force_authenticate(user=user2)
    request = API.get(f"/user/{user.id}/")
    assert request.status_code == 200


@pytest.mark.user
@pytest.mark.todo
@pytest.mark.django_db
def test_get_blocked_user(API):
    '''create table contain blocked user to prevent lookup'''
    assert 0==1


@pytest.mark.user
@pytest.mark.django_db
def test_list_user(API):
    a  = ['fady',"awad","tamer"]
    name = [str(a[randint(0,2)]+str(randint(2,50))) for _ in range(10)]
    
    users = UserFactory.create_batch(size=10,username = name)
    API.force_authenticate(user=users[0])
    request = API.get("/user/?name=fady")
    assert 200 == request.status_code

