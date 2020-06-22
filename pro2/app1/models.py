from django.db import models
from custom_user.models import User
import datetime

class Section_class(models.Model):
	year=models.CharField(max_length=20)
	div=models.CharField(max_length=10)

	def __str__(self):
		return "%s %s"%(self.year,self.div)

class Lecture(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="child_teach")
	section_class=models.ForeignKey(Section_class,on_delete=models.CASCADE)
	subject=models.CharField(max_length=20)
	lectures_conducted=models.IntegerField(null=True,default=0)

	def __str__(self):
		return "%s %s"%(self.section_class,self.subject)

class Students(models.Model):
	section=models.ForeignKey(Section_class,on_delete=models.CASCADE)
	roll=models.CharField(max_length=20,null=True)
	name=models.CharField(max_length=30)
	email=models.EmailField(max_length=50)
	lectures_attended=models.IntegerField(null=True,default=0)

	def __str__(self):
		return "%s %s"%(self.roll,self.name)



class Attendance(models.Model):
	date=models.DateField(default=datetime.date.today)
	lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE)
	students_present=models.ManyToManyField(Students)



