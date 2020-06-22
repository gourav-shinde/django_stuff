from django.contrib import admin
from django.urls import path,include
from custom_user.views import (registeration_view,logout_view,login_view,account_view
,student_loginview)
app_name="custom_user"
urlpatterns = [
	path('',registeration_view,name="register"),

	path('logout',logout_view,name="logout"),

	path('login',login_view,name="login"),
	path('student_login',student_loginview,name="studlogin"),

	path('profile',account_view,name="account"),
	
]
