import pytest
from myapi.tests.factories import *


@pytest.mark.django_db
@pytest.mark.course
#@pytest.mark.service
@pytest.mark.parametrize("authenicated",[True,False])
def test_courses_view_list(API,authenicated):
    user = UserFactory.create()

    if authenicated:
        API.force_authenticate(user=user)
    else :
        pass

    course = CourseFactory.create(owner=user)
    request = API.get(f"/course/?search={user.first_name}")
    status = request.status_code
    print(request.data)
    assert status == 200 if authenicated else status == 403
    

@pytest.mark.django_db
@pytest.mark.course
#@pytest.mark.service
@pytest.mark.parametrize("owner,enrolled",
    [(True,False),(True,True),(False,True),(False,False)]
)
def test_courses_view_reterive(API,owner,enrolled):
    if not owner and not enrolled:
        '''forbidden for user who not enrolled or not owner'''
        user = UserFactory.create()
        API.force_authenticate(user=user)
        course = CourseFactory.create()
    elif owner :
        user = UserFactory.create(is_staff=1)
        API.force_authenticate(user=user)
        course = CourseFactory.create(owner=user)
    elif enrolled:
        user = UserFactory.create()
        API.force_authenticate(user=user)
        course = CourseFactory.create()
        user.courses.add(course)
        user.save()

    request = API.get(f"/course/{course.id}/")
    status = request.status_code
    print(user.courses.all())
    print(status)
    assert status == 200 if owner or enrolled else status == 403
    
@pytest.mark.course
#@pytest.mark.service
@pytest.mark.django_db
def test_reterive_teacher_enrroled(API):
    """ teacher who enrolled in another course """
    user = UserFactory.create(is_staff=1)
    course = CourseFactory.create()
    user.courses.add(course)
    user.save()
    API.force_authenticate(user=user)
    request = API.get(f"/course/{course.id}/")
    assert request.status_code == 200

@pytest.mark.course
#@pytest.mark.service
@pytest.mark.django_db
def test_courses_view_create(API):
    user = UserFactory.create(is_staff=1)
    data = {"name":"hello world"}
    API.force_authenticate(user=user)
    request = API.post("/course/",data=data,format='json')
    result = request.data
    assert request.status_code == 201
    assert result["name"] == data["name"]
    assert result["owner"]['id'] == user.id
    



@pytest.mark.course
#@pytest.mark.service
@pytest.mark.django_db
def test_courses_view_invalid_create(API):
    user = UserFactory.create(is_staff=1)
    data = {"hello":123,"name":"hello world"}
    API.force_authenticate(user=user)
    request = API.post("/course/",data=data,format="json")
    result = request.data
    assert request.status_code == 400
    

@pytest.mark.course
#@pytest.mark.service
@pytest.mark.django_db
@pytest.mark.parametrize("teacher,student,owner",[(1,0,0),(1,0,1),(0,1,0)])
def test_courses_view_delete(API,teacher,student,owner):
    def auth(user):
        API.force_authenticate(user=user)
        req = API.delete(f"/course/{course.id}/")
        return req
    
    if teacher:
        if owner:
            user = UserFactory.create(is_staff=1)
            course = CourseFactory.create(owner=user)
            res = auth(user)
            print(res.data)
            assert res.status_code == 204
        else:
            user = UserFactory.create(is_staff=1)
            course = CourseFactory.create()
            res = auth(user)
            assert res.status_code == 403
    else:
        user = UserFactory.create()
        course = CourseFactory.create()
        res = auth(user)
        assert res.status_code == 403

             
@pytest.mark.course
#@pytest.mark.service
@pytest.mark.django_db
@pytest.mark.parametrize("teacher,student,owner",[(1,0,0),(1,0,1),(0,1,0)])
def test_courses_view_update(API,teacher,student,owner):
    def auth(user,data):
        API.force_authenticate(user=user)
        req = API.patch(f"/course/{course.id}/",data=data)
        print(req.json())
        return req

    if teacher:
        if owner:
            user = UserFactory.create(is_staff=1)
            course = CourseFactory.create(owner=user)
            res = auth(user,data={"name":"Courseraa"})
            assert res.status_code == 200
        else:
            user = UserFactory.create(is_staff=1)
            course = CourseFactory.create()
            res = auth(user,data={"name":"Courseraa"})
            assert res.status_code == 403
    else:
        user = UserFactory.create()
        course = CourseFactory.create()
        res = auth(user,data={"name":"Courseraa"})
        assert res.status_code == 403

             