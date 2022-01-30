from django.contrib.auth.models import Permission
from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.settings import import_from_string
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers, status
from ..models import Question, Quiz
from ..serializers.quiz_serializers import QuizSerializers,\
    QuizDetailSerializer , AnswerSerializer
from ..permissions import IsEnrolled, IsTeacher , IsCourseOwner
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from rest_framework.permissions import SAFE_METHODS
from .utils import REQUIRED_OWNER

class QuizViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer,BrowsableAPIRenderer]
    permission_classes = [((IsEnrolled|IsTeacher) & IsAuthenticated),]
    
    serializer_class = QuizSerializers
    def get_permissions(self):
        if self.action in REQUIRED_OWNER:
            permission_class = [IsCourseOwner,IsAuthenticated]
            return [permission() for permission in permission_class]
        return super().get_permissions()
        
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return QuizSerializers
        elif self.action  == "create":
            return QuizSerializers
        return QuizDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        '''
        Retrieve Question For Solving
        and add it To User.quizs to stop from retrieve it again
        '''
        instance = self.get_object()
        user = request.user
        exist = user.quizs.filter(id=instance.id).exists()
        if exist :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        user.quizs.add(instance)
        user.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(methods=['POST'],detail=True)
    def submit_answer(self,request,pk=None):
        ''' 
        When User Submit New Answer
        Default user_answer:0 (Wrong)
        '''
        question = Question.objects.get(id=pk)
        param = request.query_params
        data = {"point":0,"user_answer":0,
                "question":question,"user":request.user}
        try:
            answer = question.correct_answer
            if answer == param['user_answer']:
                data['point'] = question.point
                data['user_answer']= 1
                serializer = AnswerSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)
            else:
                serializer = AnswerSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

