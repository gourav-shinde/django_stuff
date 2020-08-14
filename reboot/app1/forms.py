from .models import Students,Lecture,Attendance,Section_class
from django import forms
from custom_user.models import User




class Student_form(forms.ModelForm):
	roll=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))

	name=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))

	email=forms.EmailField(max_length=50,widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))
	class Meta:
		model=Students
		fields=("roll","name","email")


class Section_class_form(forms.ModelForm):
	year=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))

	div=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))
	
	class Meta:
		model=Section_class
		fields=("year","div")

		


class Lecture_form(forms.ModelForm):
	section_class=forms.ModelChoiceField(queryset=Section_class.objects.all(), empty_label="(Select Class)",
		widget=forms.Select(
		attrs={
			'class':"form-control",
		}
		)
		)
	subject=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))
	class Meta:
		model=Lecture
		fields=('section_class','subject')
		

class Attendance_form(forms.ModelForm):
	students_present=forms.ModelMultipleChoiceField(queryset=Students.objects.all(),widget=forms.CheckboxSelectMultiple,required=True)

	def __init__(self,my_id,*args,**kwargs):
		super(Attendance_form,self).__init__(*args,**kwargs)
		var=Lecture.objects.get(id=my_id)
		print(my_id)
		print(Students.objects.filter(section=var.section_class))
		self.fields['students_present'].queryset=Students.objects.filter(section=var.section_class)

	class Meta:
		model=Attendance
		fields=("date","students_present")


class AttendanceEdit_form(forms.ModelForm):
	students_present=forms.ModelMultipleChoiceField(queryset=Students.objects.all(),widget=forms.CheckboxSelectMultiple,required=True)

	class Meta:
		model=Attendance
		fields=("date","students_present")

	


		





