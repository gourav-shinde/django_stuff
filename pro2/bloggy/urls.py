from django.contrib import admin
from django.urls import path,include
from .views import Post_view,myPost_view,editpost,post_delete,teacher_post_view
app_name="bloggy"


urlpatterns = [
	path('',Post_view,name='posts'),
	path('myPosts',myPost_view,name='myposts'),
	path('myTeachPosts',teacher_post_view,name='myTeachposts'),
	path('myTeachPosts/<int:my_id>',teacher_post_view,name='myTeachpostss'),

	path('edit/<int:my_id>',editpost,name='editpost'),
	path('delete/<int:my_id>',post_delete,name='deletepost'),

]
