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
from myapi.services.quiz import QuestionService
from myapi.views.view import CustomViewset
from myapi.mixin import CustomDispatchMixin
from myapi.permissions.permissions import QuestionPermission
from myapi.usecase.quiz import question_update , question_delete,question_create,question_list
class QuestionViewset(CustomDispatchMixin,CustomViewset):

    model = Question
    pk_url_kwarg = "pk"
    service = QuestionService
    permission = QuestionPermission

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        self.check_permission("view_question",request,obj=question)
        return Response(data=AnswerSerial.dump(question),status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        quiz_id = self.kwargs['quiz_id']
        self.check_permission("list_question",request)
        questions = question_list(quiz_id)
        return Response(data=AnswerSerial.dump(questions,many=True)\
            ,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(request.user.id)
        course = CourseService.get_by_id(self.kwargs['course_id'])
        self.check_permission("create_question",request,obj=course)
        try :
            QuestionVSerial.load(data,validate=True)
        except ValidationError as e:
            raise ParseError(detail=str(e))
        question = question_create(user=request.user,data=data)
        print(type(question.content_type))
        return Response(data=QuestionVSerial.dump(question)\
            ,status=status.HTTP_201_CREATED)

    
    def patch(self, request, *args, **kwargs):
        #TODO
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        data = request.data
        obj = self.get_object
        self.check_permission("edit_question",request,obj=obj)
        try:
            QuestionValidator.validate(data)
        except ValidationError :
            raise ParseError(detail="Invaild data")
        question = question_update(obj,data)
        return Response(data=QuestionSerial.dump(question),status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_permission("delete_question",request,obj=obj)
        question_delete(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

