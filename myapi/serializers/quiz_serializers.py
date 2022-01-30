from rest_framework import serializers
from ..models import Quiz ,Answer
from .question_serializers import QuestionSerializer

class QuizSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        depth = 0
        exclude=['users']
        
class QuizDetailSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True,read_only=True)
    class Meta :
        model = Quiz
        depth = 1
        exclude=['users','owner','end_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['created_at','id']