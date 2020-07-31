from django.contrib import admin
from .models import Students,Lecture,Attendance,Section_class
from import_export.admin import ImportExportModelAdmin

admin.site.register(Section_class)
admin.site.register(Lecture)
admin.site.register(Attendance)
# Register your models here.
@admin.register(Students)
class StudentsAdmin(ImportExportModelAdmin):
	list_display=("section","roll","name","email")
