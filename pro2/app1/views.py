from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import Students,Lecture,Attendance,Section_class
from .forms import Student_form,Lecture_form,Attendance_form,Section_class_form,AttendanceEdit_form
from custom_user.models import User
from django.contrib import messages
from tablib import Dataset
from .resources import StudentsResources
from datetime import date
# Create your views here.

def home_view(request,*args,**kwargs):     #landing page
	if not request.user.is_anonymous:
		if request.user.is_teacher:
			return redirect("app1:lectures")
		elif request.user.is_student:
			return redirect("app1:studprof")

	return render(request,"base.html",{})

def base_view(request,*args,**kwargs):
	users=User.objects.all()
	return render(request,"base_root.html",{'obj':users})


def section_view(request):    #adding new class and list of classes
	listo=Section_class.objects.all()
	form=Section_class_form(request.POST or None)
	if form.is_valid():
		form.save()
		form=Section_class_form()
		return HttpResponseRedirect("")     #redirects to current page

	context={"form":form,"list":listo,"flag":1,"title":"Add Class"}
	return render(request,"classes.html",context)

def section_delete(request,my_id):         #delete class
	obj=get_object_or_404(Section_class,id=my_id)
	print(my_id)
	if request.POST:
		obj.delete()
		return redirect("app1:section")
	context={
	"object":obj
	}
	return render(request,"delete_plug.html",context)

def section_edit(request,my_id):		#edit class
	obj=get_object_or_404(Section_class,id=my_id)
	print(my_id)
	form=Section_class_form(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		return redirect("app1:section")
	context={
	"form":form,"title":obj
	}
	return render(request,"from.html",context)




def student_view(request):     #shows all classes in which students exist
	obj=Section_class.objects.all()
	context={"list":obj}
	return render(request,"stud.html",context)



def attendance_view(request):      #attendance form
	form=Attendance_form(request.POST or None)
	if form.is_valid():
		form.save()
		form=Attendance_form()

	context={"form":form}
	return render(request,"from.html",context)



def lecture_view(request):   #adding new lecture
	print(request.user)
	print(request.user.id)
	if request.POST:
		form=Lecture_form(request.POST or None)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.user=request.user
			print(instance.user)
			instance.save()
			return redirect("app1:lectures")
	else:
		form=Lecture_form()
	context={"form":form,"title":"Create Lecture"}
	return render(request,"from.html",context)


# @login_required
def lecturelist_view(request):  #views list of lectures
	instance=request.user
	print(instance.id)
	obj=Lecture.objects.filter(user__id=instance.id)
	if request.POST:
		form=Lecture_form(request.POST or None)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.user=request.user
			print(instance.user)
			instance.save()
			return redirect("app1:lectures")
	else:
		form=Lecture_form()
	context={"lecture":obj,"form":form}
	return render(request,"vieww.html",context)



def delete_lect_view(request,my_id):   #deletes lecture
	obj=get_object_or_404(Lecture,id=my_id)
	print(my_id)
	if request.POST:
		obj.delete()
		return redirect("app1:lectures")
	context={
	"object":obj
	}
	return render(request,"delete_lecture.html",context)



def edit_lect_view(request,my_id):    #edits lecture
	obj=get_object_or_404(Lecture,id=my_id)
	print(my_id)
	form=Lecture_form(request.POST or None,instance=obj)
	form.fields['section_class'].disabled=True
	if form.is_valid():
		form.save()
		return redirect("app1:lectures")
	context={
	"form":form,"title":obj
	}
	return render(request,"from.html",context)



def stud_upload(request,my_id):      #upload students to class
	if request.POST:
		student_resource=StudentsResources()
		dataset=Dataset()
		if len(request.FILES)!=0:
			new_student=request.FILES['myfile']
		else:
			return render(request,"upload.html",{"error":"File Not Selected"})


		if not new_student.name.endswith("xlsx"):
			messages.info(request,"Wrong Format")
			return render(request,"upload.html")
		else:
			imported_data=dataset.load(new_student.read(),format="xlsx")

			for data in imported_data:
				value=Students(
					data[0],   #id
					my_id,			#section
					data[1],	#roll
					data[2],	#name
					data[3]	#email
					)
				value.save()
			ret=ret="/app1/student/"+str(my_id)+"/view"
			return redirect(ret)

	return render(request,"upload.html")


def student_detail_view(request,my_id):
	class_=Section_class.objects.get(id=my_id)
	obj=Students.objects.filter(section=my_id)
	if request.POST:								#add student within current class
		form=Student_form(request.POST or None)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.section=Section_class.objects.get(id=my_id)
			instance.save()
			return HttpResponseRedirect("")     #redirects to current page
	else:
		form=Student_form()
	context={"section":obj,"form":form,"class":class_}
	return render(request,"students_view.html",context)


def student_delete_view(request,my_id):
	obj=get_object_or_404(Students,id=my_id)
	section=obj.section
	
	print(my_id)
	if request.POST:
		obj.delete()
		ret="/app1/student/"+str(section.id)+"/view"
		return redirect(ret)
	context={
	"object":obj
	}
	return render(request,"delete_lecture.html",context)




def student_edit_view(request,my_id):
	obj=get_object_or_404(Students,id=my_id)
	section=obj.section
	print(my_id)
	form=Student_form(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		ret="/app1/student/"+str(section.id)+"/view"
		return redirect(ret)
	context={
	"form":form,"title":obj.name
	}
	return render(request,"from.html",context)



def add_attendance_view(request,my_id):
	var=Lecture.objects.get(id=my_id)
	print(my_id)
	print(Students.objects.filter(section=var.section_class))
	print("######")
	today=date.today()
	today=today.strftime("%Y-%m-%d")
	print(today)
	if request.POST:								
		form=Attendance_form(my_id,request.POST,initial={'date':today})
		print(form)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.lecture=Lecture.objects.get(id=my_id)
			print("##################")
			print(instance.date)
			print(instance.lecture)
			instance.save()
			form.save_m2m()
			return redirect("app1:attendance")
	else:
		form=Attendance_form(my_id)

	context={"form":form,"new":"Add attendence","date":today}
	return render(request,"from.html",context)



def attendance_listview(request):
	instance=request.user
	print(instance.id)
	obj=Lecture.objects.filter(user__id=instance.id)
	context={"lecture":obj}
	return render(request,"attendance_views.html",context)

def attendance_detailview(request,my_id):

	#dates
	obj=Attendance.objects.filter(lecture=Lecture.objects.get(id=my_id)).order_by("date")
	print(obj)

	#student list
	sect=Lecture.objects.get(id=my_id)
	print(sect.section_class.id)
	students=Students.objects.filter(section=sect.section_class.id)

	#presenty
	listo=[]
	present=[]
	for date in obj:
		list_of_present=date.students_present.all()
		present=[]
		for stud in students:
			flag=1
			for stud_present in list_of_present:
				if stud.id==stud_present.id:
					flag=0
					present.append("present")
			if flag==1:
				present.append("absent")

		listo.append(present)


	context={"model":obj,"stud":students,"presenty":listo,"class":sect}
	return render(request,"attendance_detail.html",context)


def attendance_dayview(request,my_id):
	obj=Attendance.objects.get(id=my_id)
	print(my_id)
	print("######")
	print(obj.lecture.section_class.id)
	print("######")
	students=Students.objects.filter(section=obj.lecture.section_class.id)
	list_of_present=obj.students_present.all()
	for stud_present in list_of_present:
		print(stud_present.id)
	print("#########")
	present=[]
	for stud in students:
		print(stud.id)

	for stud in students:
		flag=1
		for stud_present in list_of_present:
			if stud.id==stud_present.id:
				flag=0
				present.append("present")
		if flag==1:
			present.append("absent")
		


	context={"model":obj,'student':students,"presenty":present}
	return render(request,"attendance_dayview.html",context)


def edit_attendance(request,my_id):
	obj=Attendance.objects.get(id=my_id)
	print(obj)
	print(my_id)
	form=AttendanceEdit_form(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		return redirect("../../")
	context={
	"form":form,"title":obj.date
	}
	return render(request,"from.html",context)


def delete_attendance(request,my_id):
	obj=get_object_or_404(Attendance,id=my_id)
	print(my_id)
	if request.POST:
		obj.delete()
		return redirect("../../")
	context={
	"object":obj.date
	}
	return render(request,"delete_lecture.html",context)




	

####################################################################


#students views


def profile_view(request):
	instance=request.user
	stud_in_attend=Students.objects.get(email=instance.email)
	lectures_attending=Lecture.objects.filter(section_class=stud_in_attend.section)
	percentages=[0]*lectures_attending.count()
	lect_num=0
	for lect in lectures_attending:
		obj=Attendance.objects.filter(lecture=Lecture.objects.get(id=lect.id))
		count=0
		divider=1
		for day in obj:
			list_of_present=day.students_present.all()
			#print("######")
			#print(list_of_present)
			for stud in list_of_present:
				flag=1
				if stud_in_attend.id==stud.id:
					flag=0
					count=count+1
					break
		if not obj.count()==0:
			divider=obj.count()

		per=round(((count/divider)*100),2)
		percentages[lect_num]={"lect":lect,"per":per}
		lect_num=lect_num+1

	#print(percentages)
		




	context={"obj":stud_in_attend,"lecture":percentages,"instance":instance}
	return render(request,"studentprofile.html",context)

