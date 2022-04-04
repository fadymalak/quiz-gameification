from django.contrib.auth.models import Permission
from django.http.response import JsonResponse
from django.db import transaction
from django.db.models import Q, Prefetch
from django.urls import resolve
import time
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries
from rest_framework.decorators import permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.settings import import_from_string
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers, status
from ..models import Quiz
from ..models2 import *
from ..serializers.quiz_serializers import (
    QuizSerializers,
    QuizDetailSerializer,
    AnswerSerializer,
    SubmitAnswerSerializer,
)
from ..permissions import *
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny, AND, OR
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.permissions import SAFE_METHODS
from .utils import REQUIRED_OWNER


class QuizViewSet(ModelViewSet):
    """
    Viewset to ``list/update/delete`` quiz
        ``retieve`` quiz Question
        and ``submit_answer`` for question
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [IsEnrolledOrTeacher, IsAuthenticated]

    serializer_class = QuizSerializers

    def get_permissions(self):
        print(self.request.query_params)
        if self.action in REQUIRED_OWNER:
            permission_class = [IsQuizOwner, IsAuthenticated]
            return [permission() for permission in permission_class]
        print(super().get_permissions())
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in REQUIRED_OWNER or self.action == "list":
            return QuizSerializers
        return QuizDetailSerializer

    def get_queryset(self):
        print("hlllo")
        if self.action in REQUIRED_OWNER:
            print("hlllo2")
            pk = resolve(self.request.path_info).kwargs["pk"]
            print("hlllo3")
            quiz = Quiz.objects.filter(id=pk)
            print("count ->", quiz)
            return quiz
        return Quiz.objects.all()

    def perform_create(self, serializer):
        """
        ``perform_create`` is called after ``.is_vaild()`` in ``create`` method
        """
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve question from quiz to solve it (user click start quiz)
        and add it To User.quizs to stop from retrieve it again
        """
        quiz_id = self.kwargs[self.lookup_field]
        user = request.user
        exist = user.quizs.filter(id=quiz_id).exists()
        if exist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        instance = (
            Quiz.objects.filter(id=self.kwargs["pk"])
            .select_related("owner", "course")
            .prefetch_related("questions", "questions__item", "questions__item__owner")
            .get()
        )
        user.quizs.add(instance)
        serializer = self.get_serializer(instance)
        result = serializer.data

        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data["course"] = data["course"]["id"]
        serial = self.get_serializer(instance, data=data, partial=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(data=serial.data)

    def update(self, request, *args, **kwargs):
        print("Before update2")
        return super().update(request, *args, **kwargs)

    @transaction.atomic
    @action(
        methods=["POST",],
        detail=True,
        url_name="submit_asnwer",
        url_path="submit-answer",
        permission_classes=[IsEnrolledOrTeacher],
    )
    def submit_answer(self, request, pk):
        """
        When User Submit New Answer
        Default user_answer:0 (Wrong)
        """

        # questions = SubmitAnswerSerializer(data=request.data)
        # questions.is_valid(raise_exception=True)
        # questions = questions.validated_data
        # print(type(questions))
        # print(questions)
        questions = request.data
        # print(questions['data'][0])
        for param in questions:
            question = get_object_or_404(Question, id=param["id"])
            data = {
                "point": 0,
                "user_answer": "",
                "question": question.id,
                "user": request.user.id,
                "status": "COMPLETED",
            }

            try:

                answer = question.item.correct_answer
                if isinstance(question.item, GQ):
                    # manual grade for GeneralQuestion/paragraph
                    data["status"] = "PENDING"
                print("type of question ->", str(answer), type(answer))
                print(
                    "type of answer ->",
                    str(param["user_answer"]),
                    type(param["user_answer"]),
                )
                if answer == str(param["user_answer"]):
                    # Add points to user if ``correct answer`` else keep point = 0
                    data["point"] = question.point
                data["user_answer"] = param["user_answer"]
                serializer = AnswerSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
