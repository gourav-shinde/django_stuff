from django.db import models
from app1.models import Section_class
from custom_user.models import User
from datetime import datetime
# Create your models here.




class Post(models.Model):
	section=models.ForeignKey(Section_class,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date_posted=models.DateTimeField(auto_now_add=True)
	title=models.CharField(max_length=50)
	description=models.TextField()
	upvote=models.IntegerField(default=0)


	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-id',]

	