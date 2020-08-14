from django.conf import settings
from django.db import models
from custom_user.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from app1.models import Lecture
from datetime import datetime


class Quiz(models.Model):
	lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=70)
	slug = models.SlugField(blank=True,unique=True)
	roll_out_time = models.DateTimeField(default=datetime.now,blank=True)
	stop_time = models.DateTimeField(default=datetime.now,blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	pointer=models.BooleanField(default=False,blank=True,null=True)

	class Meta:
		ordering = ['timestamp',]
		verbose_name_plural = "Quizzes"

	def __str__(self):
		return self.name

class Quiz_point(models.Model):
	quiz_fro=models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name="source")
	quiz_to=models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name="points")


class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	label = models.CharField(max_length=5000)
	order = models.IntegerField(default=0)
	img1=models.ImageField(upload_to="question",blank=True,null=True)

	def __str__(self):
		return self.label


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	img=models.ImageField(upload_to="answers",null=True,blank=True)
	label = models.CharField(max_length=1500)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.label


class QuizTaker(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)
	

	def __str__(self):
		return self.user.email


class UsersAnswer(models.Model):
	quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.question.label


@receiver(pre_save, sender=Quiz)
def slugify_name(sender, instance, *args, **kwargs):
	name=instance.name+"_"+str(instance.lecture)
	instance.slug = slugify(name)