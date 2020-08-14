"""pro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app1.views import base_view,home_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',home_view,name="root"),
	path('base',base_view,name="home1"),
    path('admin/', admin.site.urls),
    path('app1/', include('app1.urls'),name="app1"),
    path('account/', include('custom_user.urls'),name="custom_user"),
    path('attendance_manage/', include('attendance_manager.urls'),name="attendance_manager"),
    path('posts/', include('bloggy.urls'),name="bloggy"),
    path('quiz/', include('quizzes.urls'),name="quizzes"),
    path('api-auth/', include('rest_framework.urls'))
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)