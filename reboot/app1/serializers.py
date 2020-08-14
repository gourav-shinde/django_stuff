from rest_framework import serializers
from .models import Students,Section_class,Lecture
from custom_user.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model =Students
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section_class
        fields=['id','year','div']

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model =Lecture
        fields="__all__"

