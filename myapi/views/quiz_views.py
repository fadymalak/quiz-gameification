from django.contrib.auth.models import Permission
from django.http import Http404
from django.http.response import JsonResponse
from django.db import transaction
from django.db.models import Q, Prefetch
from django.urls import resolve
import time
from requests import delete

from telegram import PassportElementErrorSelfie
from myapi.serializers.course_serializers import CourseSerial
from myapi.services.course import CourseService
from myapi.services.quiz import AnswerService, QuestionService, QuizService
from django.shortcuts import get_object_or_404 , get_list_or_404
from django.db import connection, reset_queries
from rest_framework.decorators import permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.decorators import  api_view
from rest_framework.settings import import_from_string
from rest_framework.viewsets import  ViewSet 
from rest_framework import serializers, status
from ..models import Quiz , Answer
from ..models2 import *
from ..serializers.quiz_serializers import (
    QuizSerial , AnswerSerial , QuizDetailSerial
    
)
from serpyco import Serializer
from myapi.usecase.quiz import answer_list, quiz_create, quiz_get,\
 quiz_list, quiz_update,quiz_delete,answers_create,answers_delete
from ..perm import *
from django.views.generic.detail import SingleObjectMixin
from rest_framework.decorators import action
from myapi.mixin import PermissionMixin , OnlyUserMixin ,CustomDispatchMixin
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer 

from rest_framework.generics import ListAPIView
from myapi.permissions.permissions import QuizPermission , AnswerPermission
from myapi.views.view import CustomViewset 

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class QuizViewSet(CustomDispatchMixin,OnlyUserMixin,PermissionMixin,SingleObjectMixin,ViewSet):
    """
    Viewset to ``list/update/delete`` quiz
        ``retieve`` quiz Question
        and ``submit_answer`` for question
    """
    service = QuizService
    permission = QuizPermission
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    model = Quiz
    pk_url_kwarg = "pk"

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        course = CourseService.get_by_id_o(self.kwargs['course_id'])
        self.check_permission("create_quiz",request,obj=course)
        quiz = quiz_create(**data,owner=user)
        return Response(data=QuizSerial.dump(quiz),status=status.HTTP_201_CREATED)

    def get(self,request,*args,**kwargs):
        """
        Retrieve question from quiz to solve it (user click start quiz)
        and add it To User.quizs to stop from retrieve it again
        """
        user = request.user
        quiz_id = kwargs[self.pk_url_kwarg]
        obj = quiz_get(quiz_id,user)
        self.check_permission("view_quiz",request,obj=obj)
        return Response(
                    QuizDetailSerial.dump(obj),
                        status=status.HTTP_200_OK
                        )

    def list(self, request, *args, **kwargs):
        ''' List Quiz by Course id'''
        course_id = kwargs.get("course_id",None)
        course= CourseService.get_by_id_o(course_id)
        self.check_permission("list_quiz",request,obj=course)
        if course_id is not None:
            data = quiz_list(course_id)
            return Response(QuizSerial.dump(data,many=True),status=status.HTTP_200_OK)
        raise Http404

    def put(self,request,*args,**kwargs): 
        raise Http404

    def patch(self,request,*args,**kwargs):
        obj = self.get_object()
        self.check_permission("edit_quiz",request,None,obj)
        data = request.data
        update = quiz_update(data,obj)
        return Response(QuizSerial.dump(update),status=status.HTTP_200_OK)

    def delete(self,request,*args,**kwargs):
        quiz_id = self.kwargs[self.pk_url_kwarg]
        quiz = QuizService.get_by_id(quiz_id)
        self.check_permission("delete_quiz",request,obj=quiz)
        quiz = quiz_delete(quiz_id)
        if quiz:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class AnswerViewset(CustomDispatchMixin,CustomViewset):
    service = AnswerService
    pk_url_kwarg: str = "pk"
    model: Model = Answer
    permission: BasePermission = AnswerPermission
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        answer = AnswerService.get_by_id(self.kwargs[self.pk_url_kwarg])

        self.check_permission("view_answer",request,obj=answer)
        return Response(data=AnswerSerial.dump(answer),status=200)

    def list(self, request, *args, **kwargs):
        quiz = QuizService.get_by_id(self.kwargs['quiz_id'])
        self.check_permission("list_answer",request,obj=quiz)
        answers = answer_list(request.user,quiz)
        answers = [answer for answer in answers]
        return Response(data=AnswerSerial.dump(answers,many=True),status=200)
        
    # @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        When User Submit New Answer
        Default user_answer:0 (Wrong)
        """
        quiz = QuizService.get_by_id(self.kwargs['quiz_id'])
        self.check_permission("create_answer",request,obj=quiz)
        answers = answers_create(request)
        return Response(data=AnswerSerial.dump(answers,many=True),status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, *args, **kwargs):
        course_id = self.kwargs['course_id']
        answer_id = self.kwargs[self.pk_url_kwarg]
        course = CourseService.get_by_id_o(course_id)
        self.check_permission("delete_answer",request,obj=course)
        answer = AnswerService.get_by_id(answer_id)
        answers = answers_delete(answer,request.user)
        return Response(data=answers,status=status.HTTP_204_NO_CONTENT)