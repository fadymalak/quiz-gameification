import pytest
from myapi.tests.factories import *

@pytest.mark.django_db
def test_courses_view_reterive(API):
    user = UserFactory.create()

    API.force_authenticate(user=user)

    course = CourseFactory.create(owner=user)
    request = API.get(f"/course/?search={user.first_name}")

    assert len(request.data) == 1
    