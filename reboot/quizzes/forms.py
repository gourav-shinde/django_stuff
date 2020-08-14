from .models import (Quiz,Question,Answer,QuizTaker,UsersAnswer)
from django import forms
from custom_user.models import User
from app1.models import Lecture



class Quiz_form(forms.ModelForm):
	name=forms.CharField(widget=forms.TextInput(
	attrs={
		'class':"form-control",
	}
	))
	lecture=forms.ModelChoiceField(queryset=Lecture.objects.all(), empty_label="(Select Class)",
	widget=forms.Select(
	attrs={
		'class':"form-control",
	}
	))
	description=forms.CharField(widget=forms.Textarea(attrs={
		'class':"form-control",'row':'1'
	}
	))
	class Meta:
		model=Quiz
		fields=('lecture','name','description','roll_out_time','stop_time')


class Answer_form(forms.ModelForm):
	label=forms.CharField(widget=forms.TextInput(
	attrs={
		'class':"form-control",
	}
	))
	
	class Meta:
		model=Answer
		fields=('label','img')





	


		





