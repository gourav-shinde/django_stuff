from django.contrib import admin
from .models import Students,Lecture,Attendance
from import_export.admin import ImportExportModelAdmin

admin.site.register(Lecture)
admin.site.register(Attendance)
# Register your models here.
@admin.register(Students)
class StudentsAdmin(ImportExportModelAdmin):
	list_display=("section","roll","name","email")
