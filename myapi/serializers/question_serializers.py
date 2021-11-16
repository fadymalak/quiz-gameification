from rest_framework import serializers
from ..models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['created_at','quiz','correct_answer']