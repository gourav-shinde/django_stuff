from django.contrib import admin
from django.urls import path,include
from .views import (Post_view,myPost_view,editpost,post_delete,teacher_post_view,student_posts,
					#json
                    posts,create_post)
app_name="bloggy"


urlpatterns = [
	path('',Post_view,name='posts'),

	path('myPostApi/<int:my_id>',posts),

	path('myPosts',myPost_view,name='myposts'),
	path('myClass',student_posts,name='studentposts'),#api 
	path('myClass/create',create_post),#api 
	path('myTeachPosts',teacher_post_view,name='myTeachposts'),
	path('myTeachPosts/<int:my_id>',teacher_post_view,name='myTeachpostss'),

	path('edit/<int:my_id>',editpost,name='editpost'),
	path('delete/<int:my_id>',post_delete,name='deletepost'),

]
