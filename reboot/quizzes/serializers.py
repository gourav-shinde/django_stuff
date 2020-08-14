from .models import QuizTaker,Quiz
from rest_framework import serializers


class QuizTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizTaker
        fields=['quiz']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields="__all__"