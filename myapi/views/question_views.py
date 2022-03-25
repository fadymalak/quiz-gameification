from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from myapi.models2 import *
from myapi.serializers.quiz_serializers import AnswerSerializer
from rest_framework import status
from rest_framework.response import Response 




class QuestionViewset(ModelViewSet):

    #submit single question
    @action(methods=['POST'],detail=True)
    def submit_answer(self,request,pk=None):

        ''' 

        When User Submit New Answer

        Default user_answer:0 (Wrong)

        '''

        question = Question.objects.get(id=pk)

        param = request.data

        data = {"point":0,"user_answer":"",

                "question":question,"user":request.user,"status":"COMPLETED"}



        try:

            answer = question.item.correct_answer

            

            if isinstance(question.item,GQ):

                #manual grade for GeneralQuestion/paragraph

                data['status'] = "PENDING"



            if answer == param['user_answer']:

                # Add points to user if ``correct answer`` else keep point = 0

                data['point'] = question.point



            data['user_answer'] = param['user_answer']

            serializer = AnswerSerializer(data=data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(data=serializer.data,

                status=status.HTTP_201_CREATED)

        except:

            return Response(status=status.HTTP_400_BAD_REQUEST)
