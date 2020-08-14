from django.contrib import admin
from django.urls import path
from .views import (student_view,lecture_view,attendance_view,home_view,lecturelist_view,section_view,delete_lect_view,
	edit_lect_view,stud_upload,student_detail_view,student_delete_view,student_edit_view,add_attendance_view,attendance_listview,
	attendance_detailview,attendance_dayview,edit_attendance,section_delete,section_edit,profile_view,delete_attendance,
	add_rem_teach,student_profile,teach_json,
	#JSON VIEWS
	lecture_jview,section_jview
)
app_name="app1"
urlpatterns = [
	# json links
path("json",teach_json),###
path("jlecture",lecture_jview),
path("jsection",section_jview),

# endjson
path('',home_view,name="home2"),
path('attendance/',attendance_listview,name="attendance"),
path('attendance/<int:my_id>/view',attendance_detailview,name="attendance_detail"),
path('attendance_day/<int:my_id>/day',attendance_dayview,name="attendance_day"),
path('attendance_day/<int:my_id>/edit',edit_attendance,name="edit_attendance"),
path('attendance_day/<int:my_id>/delete',delete_attendance,name="delete_attendance"),

path('lecture/',lecture_view,name="lecture"),
path('student/',student_view,name="student"),
path('lectview/',lecturelist_view,name="lectures"),

path('sectview/',section_view,name="section"),
path('sectview/<int:my_id>/delete',section_delete,name="section_delete"),
path('sectview/<int:my_id>/upload',stud_upload,name="upload"),
path('sectview/<int:my_id>/edit',section_edit,name="section_edit"),
path('sectview/<int:my_id>/teachers',add_rem_teach,name="section_teacher"),


path('lectview/<int:my_id>/delete',delete_lect_view,name="delete_lect"),
path('lectview/<int:my_id>/edit',edit_lect_view,name="edit_lect"),

path('student/<int:my_id>/view',student_detail_view,name="stud_view"),
path('student/<int:my_id>/view/delete',student_delete_view,name="stud_delete"),
path('student/<int:my_id>/view/edit',student_edit_view,name="stud_edit"),
path('attendance/<int:my_id>',add_attendance_view,name="add_attendance"),


##student views
path('profile',student_profile,name="studprof"),##mainview template
path('Studentprofile',profile_view,name="studprofile"), ##hometab json link

]
