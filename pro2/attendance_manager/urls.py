from django.contrib import admin
from django.urls import path

from .views import To_view,section_attendance


app_name="attendance_manager"
urlpatterns = [
path('<int:my_id>',To_view,name="viewer"),
path('class/<int:my_id>',section_attendance,name="class_viewer"),

]