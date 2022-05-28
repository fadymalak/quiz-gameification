
import itertools
from typing_extensions import Self
from myapi.services.service import Service
from myapi.models import Quiz , Answer , Question
from myapi.models2 import BaseItem
from typing import List
from myapi.services.course import CourseService
def _queryset_to_list(queryset):
    result = []
    for obj in queryset:
        result.append(obj)
    return result
class QuizService(Service):

    def get_by_id(qid:int ) -> Quiz:
        quiz  = Quiz.objects.filter(id=qid).get()
        return quiz

    def get_detials_by_id(qid:int ) -> Quiz:
        quiz  = Quiz.objects\
             .select_related("owner", "course")\
                    .prefetch_related("questions", "questions__item", "questions__item__owner")\
                        .filter(id=qid).get()
        return quiz

    def list_active_by_course_id(course_id:int) -> List[Quiz]:
        quizs = Quiz.objects.filter(course__id = course_id).all()
        quiz_iter = _queryset_to_list(quizs)
        return quiz_iter

    def create(**kwargs) -> Quiz:
        quiz = Quiz.objects.create(**kwargs)
        return quiz


    def update(quiz:Quiz ,**kwargs) -> Quiz:
        '''Update Quiz
        :param quiz: Quiz instance
        :param **kwargs: data to update
        
        '''
        updated = 0
        update_fields = []
        for k,v in kwargs.items():
            if k not in  ["questions","course","owner","id"] :
                print(k)
                if getattr(quiz,k) != v :
                   setattr(quiz,k,v)
                   update_fields.append(k)
                   updated= 1

        quiz.save()
        return  quiz



def _filter_by_quiz_id(quiz_id):
    return Question.objects.filter(quiz__id=quiz_id)

class QuestionService(Service):

    def get_by_id(id:int ) -> Question:
        question  = Question.objects.get(id=id)
        return question

    def get_by_ids( ids : list[int] ) :
        questions = Question.objects.prefetch_related("item")\
                    .select_related("content_type").filter(id__in =ids).all()
        return questions

    def get_ids_by_quiz_id(quiz_id:int) -> List[int]:
        questions = _filter_by_quiz_id(quiz_id)\
                        .values_list("id",flat=True).all()
        return list(questions)

    def get_by_quiz_id(quiz_id:int) -> List[Question]:
        queryset = _filter_by_quiz_id(quiz_id)\
                                .prefetch_related("item")\
                                    .select_related("content_type").all()
        questions = [question for question in queryset]
        return questions

    def create(user,**kwargs) -> Question:
        item_data = kwargs.pop("item")
        item_type = kwargs.pop("content_type")['model'].lower()
        quiz_id = kwargs.pop("quiz")['id']
        quiz = QuizService.get_by_id(quiz_id)
        item = None
        for q_type in BaseItem.__subclasses__():
            #find content-type Question type and creat it
            if item_type in q_type.__name__.lower():
                item = q_type(**item_data)
                item.owner = user
                item.save() 
        #create_question
        question = Question(item=item,quiz=quiz,point=kwargs['point'])
        question.save()
        return question

    def update(question:Question ,**kwargs) -> Exception:
        raise NotImplementedError()





class AnswerService(Service):
    
    def get_by_id(id:int ) -> Answer:
        answer  = Answer.objects.get(id=id)
        return  answer

    def filter_by_user_and_question(user,ids:list[int]):
        answers = Answer.objects.filter(question__id__in=ids,user=user).all()
        return answers
        
    def create(**kwargs) -> Answer:
        answer = Answer.objects.create(**kwargs)
        return answer

    def create_bulk(data:List[dict]) -> List[Answer] :
        answers = Answer.objects.bulk_create(data)
        return answers

    def update(Quiz:Quiz ,**kwargs) -> Exception:
        raise NotImplementedError()