from django.contrib import admin
from django.urls import path,include
from custom_user.views import (registeration_view,logout_view,login_view,account_view
,student_loginview,newregister,wait,verification,passy)
app_name="custom_user"
urlpatterns = [
	path('pass',passy,name="passy"),
	path('',registeration_view,name="register"),
	path('register',newregister,name="newregister"),
	path('wait',wait,name="wait"),
	path('activate/<uidb64>/<token>',verification,name="activate"),


	path('logout',logout_view,name="logout"),

	path('login',student_loginview,name="login"),
	path('student_login',student_loginview,name="studlogin"),

	path('profile',account_view,name="account"),
	
]
