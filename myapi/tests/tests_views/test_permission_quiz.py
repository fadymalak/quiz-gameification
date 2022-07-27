from flask_login import user_loaded_from_cookie
from rest_framework.test import APIClient
import pytest
from myapi.serializers.quiz_serializers import QuizDetailSerial as QuizDetailSerializer
from myapi.tests.utils import gen_quiz_data
from myapi.tests.factories import *
from django.test.utils import CaptureQueriesContext
from django.db import connection
import datetime
from rest_framework import status


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.quiz
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 201), (False, False, 403), (False, True, 201), (True, False, 403)],
)
def test_acceptance_CREATE_quiz_endpoint(API, teacher, own, result):
    u = UserFactory.create(is_staff=teacher)
    if own == False :
        """
        test if other teacher (not owner of course)
            can create quiz in courses not owing them
        """
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner=u1)
    else:
        c = CourseFactory.create(owner=u)

    API.force_authenticate(user=u)
    data = gen_quiz_data(
        title="Quiz%s" % (str(teacher)),
       # owner=u.id,
        course=c.id,
        end_at=str(datetime.datetime.now()),
    )
    request = API.post(f"/course/{c.id}/quiz/", data=data)
    print(f'{request.data=}')
    assert  result == request.status_code


@pytest.mark.test
@pytest.mark.quiz
@pytest.mark.django_db
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 204), (False, False, 403), (False, True, 204), (True, False, 403)],
)
def test_acceptance_DELETE_quiz_endpoint(API, teacher, own, result):
    u = UserFactory.create(is_staff=teacher)
    if own == False :
        """
        test if other teacher (not owner of course)
            can :delete: quiz in courses not owing them
        """
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner=u1)
        quiz = QuizFactory.create(owner=u1, course=c)

    else:
        c = CourseFactory.create(owner=u)
        quiz = QuizFactory.create(owner=u, course=c)

    API.force_authenticate(user=u)
    before = Quiz.objects.filter(id=quiz.id).count()
    data = {"course": c.id}
    request = API.delete(f"/course/{c.id}/quiz/{quiz.id}/")
    print(request.data)
    after_result = Quiz.objects.filter(id=quiz.id).count()
    if result != 204:
        after = 1
    else:
        after = 0
    print(request.status_code)
    assert before == 1
    assert after_result == after
    assert request.status_code == result


@pytest.mark.test
@pytest.mark.quiz
@pytest.mark.django_db
def test_acceptance_DELETE_quiz_endpoint_student(API):
    u = UserFactory.create()

    c = CourseFactory.create(owner=u)
    quiz = QuizFactory.create(owner=u, course=c)
    student = UserFactory.create()
    API.force_authenticate(user=student)
    student.courses.add(c)
    student.save()
    before = Quiz.objects.filter(id=quiz.id).count()
    data = {"course": c.id}
    request = API.delete(f"/course/{c.id}/quiz/{quiz.id}/")
    after_result = Quiz.objects.filter(id=quiz.id).count()

    print(request.status_code)
    assert before == 1
    assert after_result == 1
    assert request.status_code == 403

@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.quiz
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 200), (False, False, 403)],
)
def test_update_quiz_endpoint(API, teacher, own, result):
    u = UserFactory.create(is_staff=teacher)
    if own == False:
        """
        test if other teacher (not owner of course)
            can :delete: quiz in courses not owing them
        """
        u1 = UserFactory.create(is_staff=teacher)
        c = CourseFactory.create(owner=u1)
        quiz = QuizFactory.create(owner=u1, course=c)
    else:
        c = CourseFactory.create(owner=u)
        quiz = QuizFactory.create(owner=u, course=c)

    API.force_authenticate(user=u)
    serial = QuizDetailSerializer.dump(quiz)
    data = serial
    print(data)
    data["title"] = "QUIZOOOOO"
    request = API.patch(f"/course/{c.id}/quiz/{quiz.id}/", data={'id':data['id'],'title':data["title"]}, format="json")

    print(request.status_code)
    rdata = request.data
    print(rdata)
    print(request.context)
    print(request.content)
    if request.status_code == 200:
        assert data["title"] == rdata["title"]

    assert request.status_code == result


@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.quiz
@pytest.mark.parametrize(
    "teacher,own,result",
    [(True, True, 200), (False, False, 403), (False, True, 200), (True, False, 200)],
)
def test_retreive_quiz_endpoint(API, teacher, own, result):
    user = UserFactory.create()

    course = CourseFactory.create(owner=user)
    quiz = QuizFactory.create(course=course)
    question_item = MCQFactory.create()
    question_item2 = MCQFactory.create()
    question_item3 = GQFactory.create()
    question = QuestionFactory.create(item=question_item, quiz=quiz)
    question = QuestionFactory.create(item=question_item2, quiz=quiz)
    question = QuestionFactory.create(item=question_item3, quiz=quiz)
    if teacher :
        student = UserFactory.create()
        student.courses.add(course)
        print("#course id ",course.id)
        student.save()
        API.force_authenticate(user=student)
    if own:
        API.force_authenticate(user=user)
    if not own and not teacher :
        student = UserFactory.create()
        API.force_authenticate(user=student)

    with CaptureQueriesContext(connection) as ctx:
        req = API.get(f"/course/{course.id}/quiz/{quiz.id}/")
    x = ctx.captured_queries
    print(f"[*] length : {len(x)}")
    for i in x:
        print("-> ", i["sql"])
    
    print(req)
    print(req.data)
    assert req.status_code == result



@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.quiz
def test_retreive_anonymous_quiz_endpoint(API):
    user = UserFactory.create()

    course = CourseFactory.create(owner=user)
    quiz = QuizFactory.create(course=course)
    question_item = MCQFactory.create()
    question_item2 = MCQFactory.create()
    question_item3 = GQFactory.create()
    question = QuestionFactory.create(item=question_item, quiz=quiz)
    question = QuestionFactory.create(item=question_item2, quiz=quiz)
    question = QuestionFactory.create(item=question_item3, quiz=quiz)


    with CaptureQueriesContext(connection) as ctx:
        req = API.get(f"/course/{course.id}/quiz/{quiz.id}/")
    x = ctx.captured_queries
    print(f"[*] length : {len(x)}")
    for i in x:
        print("-> ", i["sql"])
    
    print(req)
    print(req.data)
    assert req.status_code == 401




@pytest.mark.test
@pytest.mark.django_db
@pytest.mark.quiz
@pytest.mark.parametrize(
    "student,own,result",
    [(True, True, 200), (False, False, 403), (False, True, 200)],
)
def test_list_quiz_endpoint(API, student, own, result):
    # TODO fetch only course quizs
    LENGTH = 4
    user = UserFactory.create()
    course = CourseFactory.create(owner=user)
    student1 =  UserFactory.create()
    if  student :
        #enrolled Student
        print("course added")
        student1.courses.add(course)
        student1.save()
        API.force_authenticate(user=student1)
    elif student == False :
        student2 = UserFactory.create()
        API.force_authenticate(user=student2)
    if own :
        API.force_authenticate(user=user)
    # print(course.users.all())
    print(course.owner.id)
    print(user)
    # print("3333333333333")
    # API.force_authenticate(user=student1)

    quiz = QuizFactory.create_batch(LENGTH, course=course)
    print(course.owner.id)
    req = API.get(f"/course/{course.id}/quiz/")
    print(req.data)
    assert result == req.status_code
    

@pytest.mark.django_db
@pytest.mark.answer
@pytest.mark.todo
def test_submit_invalid_answer(API):
    assert 1==0

@pytest.mark.django_db
@pytest.mark.answer 
def test_submit_answer_quiz_endpoint(API):
    user = UserFactory.create()
    mcq = MCQFactory.create()
    question = QuestionFactory.create(item=mcq)
    course = Courses.objects.first()
    API.force_authenticate(user=user)
    print(question.id)
    user.courses.add(course)
    data=[{'user_answer':mcq.correct_answer,'id':int(question.id)},]
    request = API.post(f"/course/{course.id}/quiz/{question.quiz.id}/answer/",data=data,format='json')
    print("#,",request.data)
    assert 201 == request.status_code


@pytest.mark.django_db
@pytest.mark.answer
def test_get_answer_quiz_endpoint(API):
    user = UserFactory.create()
    mcq = MCQFactory.create()
    question = QuestionFactory.create(item=mcq)
    course = Courses.objects.first()
    API.force_authenticate(user=user)
    user.courses.add(course)
    data=[{'user_answer':mcq.correct_answer,'id':int(question.id)},]
    request = API.post(f"/course/{course.id}/quiz/{question.quiz.id}/answer/",data=data,format='json')
    assert 201 == request.status_code
    request2 = API.get(f"/course/{course.id}/quiz/{question.quiz.id}/answer/{request.data[0]['id']}/")
    request3 = API.get(f"/course/{course.id}/quiz/{question.quiz.id}/answer/")

    assert request2.status_code == 200
    assert request3.status_code == 200



@pytest.mark.django_db
@pytest.mark.answer
def test_delete_answer_quiz_endpoint(API):
    user = UserFactory.create()
    mcq = MCQFactory.create()
    mcq2 = MCQFactory.create()
    question = QuestionFactory.create(item=mcq)
    question2 = QuestionFactory.create(item=mcq2,quiz = question.quiz)
    course = Courses.objects.first()
    course_owner = course.owner
    API.force_authenticate(user=user)
    user.courses.add(course)
    data=[{'user_answer':mcq.correct_answer,'id':int(question.id)},]
    request = API.post(f"/course/{course.id}/quiz/{question.quiz.id}/answer/",data=data,format='json')
    data2=[{'user_answer':mcq.correct_answer,'id':int(question2.id)},]
    req2 = API.post(f"/course/{course.id}/quiz/{question.quiz.id}/answer/",data=data2,format='json')
    assert 201 == request.status_code
    request2 = API.get(f"/course/{course.id}/quiz/{question.quiz.id}/answer/{request.data[0]['id']}/")
    request4 = API.delete(f"/course/{course.id}/quiz/{question.quiz.id}/answer/{request.data[0]['id']}/")
    strange = UserFactory.create()
    API.force_authenticate(user=strange)
    request6 = API.delete(f"/course/{course.id}/quiz/{question.quiz.id}/answer/{request.data[0]['id']}/")
    API.force_authenticate(user=course_owner)
    print(Answer.objects.all())
    request5 = API.delete(f"/course/{course.id}/quiz/{question.quiz.id}/answer/{request.data[0]['id']}/")
    print("# delted item is ",request5.data)
    print(User.objects.get(id=user.id))
    print(Courses.objects.all())
    print(Quiz.objects.all())
    print(Answer.objects.count())
    assert request6.status_code == 403
    assert request4.status_code == 403
    assert request5.status_code == 204
