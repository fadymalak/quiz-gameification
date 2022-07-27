from attr import dataclass
from myapi.models2 import Question
from myapi.models import Courses

from myapi.serializers.quiz_serializers import \
 AnswerSerial, QuestionSerial , QuestionValidator, QuestionVSerial
from myapi.serializers.serial import ValidationError
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.response import Response
from myapi.services.course import CourseService
from myapi.services.quiz import QuestionService, QuizService
from myapi.views.view import CustomViewset
from myapi.mixin import CustomDispatchMixin
from myapi.permissions.permissions import QuestionPermission
from myapi.usecase.quiz import question_update , question_delete,question_create,question_list
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from django.views.generic.detail import SingleObjectMixin
from myapi.mixin import PermissionMixin
from myapi.views.view import AbsViewset
from rest_framework.decorators import api_view

class QuestionViewset(CustomDispatchMixin,CustomViewset):

    model = Question
    pk_url_kwarg = "pk"
    service = QuestionService
    permission = QuestionPermission

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        self.check_permission("view_question",request,obj=question.quiz.course)
        return Response(data=QuestionVSerial.dump(question),status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        quiz_id = self.kwargs['quiz_pk']
        #will produce bug for course owner
        #course owner will not able to list quiz
        #need add Course check also
        course = CourseService.get_by_id(self.kwargs['course_pk'])
        self.check_permission("list_question",request,obj=course)
        questions = question_list(quiz_id)
        return Response(data=QuestionVSerial.dump(questions,many=True)\
            ,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        course = CourseService.get_by_id(self.kwargs['course_pk'])
        self.check_permission("create_question",request,obj=course)
        try :
            QuestionVSerial.load(data,validate=True)
        except ValidationError as e:
            raise ParseError(detail="Invalid data")
        question = question_create(user=request.user,data=data)
        return Response(data=QuestionVSerial.dump(question)\
            ,status=status.HTTP_201_CREATED)

    
    def partial_update(self, request, *args, **kwargs):
        #TODO
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_permission("delete_question",request,obj=obj.quiz.course)
        question_delete(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

