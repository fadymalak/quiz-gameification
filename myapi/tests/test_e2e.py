from rest_framework.test import APIClient
import pytest
import functools
from .factories import *
from myapi.models import *
from .utils import rgetattr ,gen_quiz_data


@pytest.mark.e2e
@pytest.mark.django_db
def test_e2e_courses_get_queryset(API,SUPER_LOGIN):
    user = UserFactory.create(first_name="fady",last_name="malak" , username="awad")
    user1 = UserFactory.create(first_name="michael",last_name="fahmy" , username="michoa")
    course = CourseFactory.create(owner=user)
    course1 = CourseFactory.create(owner=user1)
    req = API.get("/course/?search=malak")
    data = req.json()[0]
    assert req.status_code == 200
    assert data['owner'] == user.username
    assert data['name'] == course.name



# @pytest.mark.e2e
@pytest.mark.django_db
def test_functional_get_course_by_id(API,SUPER_LOGIN):
    user=  UserFactory.create()
    course = CourseFactory.create(owner=user)
    req = API.get("/course/%s/"%(course.id))
    data = req.json()
    print(data)
    assert data['name'] == course.name

# @pytest.mark.e2e
@pytest.mark.django_db
@pytest.mark.parametrize("attr",['owner.username','name','oname'])
def test_functional_course_get_queryset(attr,API,SUPER_LOGIN):
    courses = CourseFactory.create_batch(size = 10)
    course = courses[random.randint(1,10)]
    if attr == "oname":
        search = course.owner.first_name + " " + course.owner.last_name
    else:
        search = rgetattr(course,attr)
    req = API.get("/course/?search=%s"%(search))
    data = req.json()
    assert len(data) == 1 
    assert data[0]['owner'] ==  course.owner.username
    assert data[0]['name'] == course.name
    



@pytest.mark.e2e
@pytest.mark.django_db
def test_functional_create_user():
    API = APIClient()
    req = API.post("/users/",data={
        "first_name":"fadyaa",
        "last_name":"malaka",
        "username":"fadymalakc",
        "email":"fady.malak.awad@gmail.com",
        "password":"Fady.1234"
    })
    print(req.data)
    assert req.status_code == 201



@pytest.mark.e2e
@pytest.mark.django_db
def test_functional_Course_create(API,SUPER_LOGIN):
    rdata = {
        "name":"COURSE NUMER 2"

    }
    req = API.post("/course/",data=rdata)
    data = req.json()
    print(data)
    assert data['name'] == rdata['name']
    assert req.status_code == 201


# @pytest.mark.e2e
# @pytest.mark.parametrize("username,staff",\
#     [("fady_malak",True),("student_2022",False)])
# @pytest.mark.django_db
# def test_e2e_create_quiz(API,username,staff):
#     u = UserFactory.create(username=username,is_staff=staff)
#     API.force_authenticate(user=u)
#     req = API.post("/course/",data={"name":"Course 1"})
    

@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.parametrize("teacher,own,result",\
    [(True,True,201),(False,False,403),(False,True,403),(True,False,403)])
def test_e2e_create_quiz_endpoint(API,teacher,own,result):
    u = UserFactory.create(is_staff=teacher)
    if own == False and teacher == True:
        '''
    test if other teacher (not owner of course) 
        can create quiz in courses not owing them
        '''
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner= u1)
    else :
        c = CourseFactory.create(owner= u)

    API.force_authenticate(user=u)
    data = \
    gen_quiz_data(title="Quiz%s"%(str(teacher)),
                    owner = u.id,
                    course=c.id,
                )

    request = API.post("/quiz/",data = data)
    assert request.status_code == result


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.parametrize("user_login",[True,False],indirect=True)
def test_testo(user_login):
    a , b = user_login
    print(a)
    print(b)
    q = User.objects.all()[0]
    assert q.is_staff == b