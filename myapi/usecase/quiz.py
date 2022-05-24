from venv import create
from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework import status
from requests import delete
from myapi.services.quiz import AnswerService, QuestionService , QuizService
from myapi.services.course import CourseService
import datetime
from typing import List, Tuple , Union 
from myapi.models import Answer, Quiz , User
from myapi.models2 import GQ
class QuizOpenBeforeException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Quiz Already Opened Before"

def quiz_create(**kwargs) -> Quiz:
    data = kwargs.copy()
    data['course'] = CourseService.get_by_id_o(data['course'][0])
    quiz = QuizService.create(**data)
    return quiz

def quiz_list(course_id :int) -> List[Quiz]:
    print(course_id)
    quizs = QuizService.list_active_by_course_id(course_id=course_id)
    return quizs

def quiz_get(quiz_id:int, user: User) -> Quiz:
    '''
    Reterive quiz and add it to user
    '''
    quiz = QuizService.get_detials_by_id(quiz_id)
    #add quiz to user 
    user.quizs.add(quiz)
    return quiz


def quiz_update(data:dict,obj:Quiz) -> Quiz:
    updated = QuizService.update(obj,**data)
    return updated

def quiz_delete(quiz_id : int) -> Tuple[int,dict[str,int]]:
    quiz = Quiz.objects.get(id=quiz_id).delete()
    if quiz[0]  >= 1 :
        return True
    return False
def answer_get(id):
    answer = AnswerService.get_by_id(id)
    return answer
def answer_list(user:User,quiz:Quiz):
    questions : List[int] = QuestionService.get_by_quiz(quiz.id)
    answers = AnswerService.filter_by_user_and_question(user,questions)
    return answers

def _create_questions_list(request):
    questions = request.data
    param = {q['id']:q['user_answer'] for q in questions}
    ids = list(param.keys())
    
    answers = []
    questions = QuestionService.get_by_ids(ids)
    return questions


def answers_create(request):

    questions_dict = request.data
    param = {q['id']:q['user_answer'] for q in questions_dict}
    questions = _create_questions_list(request)
    answers_list = []

    for question in questions:
        data = {
            "point": 0,
            "user_answer": "",
            "question": question,
            "user": request.user,
            "status": "COMPLETED",
        }
        answer = question.item.correct_answer

        if isinstance(question.item, GQ):
            # manual grade for GeneralQuestion/paragraph
            data["status"] = "PENDING"

        if answer == str(param[question.id]):
            # Add points to user if ``correct answer`` else keep point = 0
            data["point"] = question.point

        data["user_answer"] = str(param[question.id])
        answers_list.append(Answer(**data))
    
    answers = Answer.objects.bulk_create(answers_list)
    return answers

def answer_delete(answer:Answer,user:User):
    '''remove answer and remove user from quiz submittion'''
    quiz = answer.question.quiz
    user.quizs.remove(quiz)
    answer.delete()

def question_create(*,type:str,):
    pass

def question_update():
    pass

def question_delete():
    pass