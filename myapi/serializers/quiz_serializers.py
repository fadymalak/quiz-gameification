from rest_framework import serializers
from myapi.models import Quiz, Answer
from myapi.serializers.question_serializers import QuestionSerializer


class QuizSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        depth = 0
        exclude = ["users"]


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        depth = 1
        exclude = ["users", "owner", "end_at"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ["created_at", "id"]


class Answer2Serializer(serializers.Serializer):
    user_answer = serializers.CharField()
    id = serializers.IntegerField()


class SubmitAnswerSerializer(serializers.Serializer):
    data = Answer2Serializer(many=True)
