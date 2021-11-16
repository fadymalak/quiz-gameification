from rest_framework import serializers
from ..models import Quiz
from .question_serializers import QuestionSerializer

class QuizSerializers(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        depth = 0
        exclude=['users']
        