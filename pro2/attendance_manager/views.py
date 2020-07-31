from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import To_fro
from .forms import To_form,ulimit_form
from app1.models import (Attendance,Lecture,Students,Section_class)
import threading
#decorator
from django.contrib.auth.decorators import login_required

class EmailThread(threading.Thread):

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=True)
	


# Create your views here.
@login_required(login_url='/account/login')
def To_view(request,my_id):    #viewing attendances and sending email to students
	form1=ulimit_form(request.POST or None,initial={'percentage':75}) #TAKING minimum % required
	lecto=Lecture.objects.get(id=my_id)
		#dates
	obj=Attendance.objects.filter(lecture=Lecture.objects.get(id=my_id)).order_by("date")
	print(obj)
	divider=obj.count()
	#student list
	if divider==0:
		divider=1
	sect=Lecture.objects.get(id=my_id)
	print(sect.section_class.id)
	students=Students.objects.filter(section=sect.section_class.id)
	calculation=[0]*students.count()
	print(calculation)
	#presenty
	listo=[]
	present=[]
		
	for date in obj:
		list_of_present=date.students_present.all()
		counter=0
		present=[]
		for stud in students:
			flag=1
			for stud_present in list_of_present:
				if stud.id==stud_present.id:
					flag=0
					present.append("present")
					calculation[counter]=calculation[counter]+1
			if flag==1:
				present.append("absent")
			counter=counter+1

		listo.append(present)

	calculations=[]
	#print(obj[0].date)
	#print(obj[(obj.count()-1)].date)
	for x in calculation:
		calculations.append(round(((x/divider)*100),2))

	if form1.is_valid():
		into=form1.save(commit=False)
		#print("hello")
		#print("################")
		counter=0
		for stud in students:
			if calculations[counter]<into.percentage:
				#send_mail(subject,message,from_email,to_email,fail_silently=True)
				subject="Defaulter in "+str(lecto)+" from "+str(obj[0].date)+" to "+str(obj[(obj.count()-1)].date)
				message="Defaulter in "+str(lecto)+" from "+str(obj[0].date)+" to "+str(obj[(obj.count()-1)].date)+"\n"+"Your attendace is "+str(calculations[counter])+"%"+"It should be above "+str(into.percentage)+"%\n"
				to_list=[stud.email]
				email = EmailMessage(subject,message,'gauravshinde696969@gmail.com',to_list)
				EmailThread(email).start()
			counter=counter+1

		return redirect('app1:attendance')

	if obj:
		form=To_form(request.POST or None,initial={'fro':obj[0].date})
	else:
		form=To_form(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		#print("#######")
		#print(instance.to)

		#dates
		obj=Attendance.objects.filter(lecture=Lecture.objects.get(id=my_id),date__range=[instance.fro,instance.to]).order_by("date")
		#print(obj.count())
		divider=obj.count()
		if divider==0:
			divider=1
		#print(type(divider))

	 	#student list
		sect=Lecture.objects.get(id=my_id)

		#print(sect.section_class.id)

		students=Students.objects.filter(section=sect.section_class.id)
		#print(students.count())

		calculation=[0]*students.count()
		#print(calculation)
		#presenty
		listo=[]
		present=[]
		
		for date in obj:
			list_of_present=date.students_present.all()
			counter=0
			present=[]
			for stud in students:
				flag=1
				for stud_present in list_of_present:
					if stud.id==stud_present.id:
						flag=0
						present.append("present")
						calculation[counter]=calculation[counter]+1
				if flag==1:
					present.append("absent")
				counter=counter+1

			listo.append(present)

		calculations=[]

		for x in calculation:
			calculations.append(round(((x/divider)*100),2))
		
		if form1.is_valid():
			#print("end")
			return redirect('app1:attendance')
	#print(form)

	context={"form":form,"stud":students,"presenty":listo,"model":obj,"cal":calculations,"dont":my_id,"title":lecto,"form1":form1}
	return render(request,"attend_viewer.html",context)

@login_required(login_url='/account/login')
def section_attendance(request,my_id):  #getting attendance of section


	

	section=Section_class.objects.get(id=my_id)
	students=Students.objects.filter(section=section.id)
	lectures=Lecture.objects.filter(section_class=section.id)
	listo=[]		#list of lect_cal
	total_list=[0]*students.count()				
	total_session_count=0
	lect_session_count=[0]*lectures.count()
	percentage=[]   #final %
	small_date=0

	for lect in lectures:
		lect_count=0
		lect_cal=[0]*students.count()  #attendace of a lecture
		obj=Attendance.objects.filter(lecture=Lecture.objects.get(id=lect.id)).order_by("date")
		if small_date==0:
			if obj:
				small_date=obj[0].date
		else:
			if obj:
				if small_date>obj[0].date:
					small_date=obj[0].date
		divider=obj.count()
		if divider==0:
			divider=1
		
		for date in obj:
			lect_session_count[lect_count]=lect_session_count[lect_count]+1
			total_session_count=total_session_count+1
			list_of_present=date.students_present.all()
			counter=0
			for stud in students:
				flag=1
				for stud_present in list_of_present:
					if stud.id==stud_present.id:
						flag=0
						lect_cal[counter]=lect_cal[counter]+1
						total_list[counter]=total_list[counter]+1
				counter=counter+1
		lect_count=lect_count+1
			
		listo.append(lect_cal)  #list of list of attendance
		lect_count=lect_count+1

	for x in total_list:
		if total_session_count==0:
			total_session_count=1
		percentage.append(round(((x/total_session_count)*100),2))

	#forms
	form1=ulimit_form(request.POST or None,initial={'percentage':75}) #TAKING minimum % required
	form=To_form(request.POST or None,initial={'fro':small_date})


	if form1.is_valid():
		into=form1.save(commit=False)
		#print("hello")
		#print("################")
		counter=0
		for stud in students:
			if percentage[counter]<into.percentage:
				#send_mail(subject,message,from_email,to_email,fail_silently=True)
				subject="Defaulter in "+str(section)
				message="You have "+str(percentage[counter])+"%.Minimum required is "+str(into.percentage)+"%"
				to_list=[stud.email]
				email = EmailMessage(
										subject,
										message,
										'gauravshinde696969@gmail.com',
										to_list
									)
				EmailThread(email).start()
				#send_mail(subject,message,"gauravshinde696969@gmail",to_list,fail_silently=True)
			counter=counter+1

		return redirect('app1:attendance')

	if form.is_valid():
		instance=form.save(commit=False)
		listo=[]		#list of lect_cal
		total_list=[0]*students.count()				
		total_session_count=0
		lect_session_count=[0]*lectures.count()
		percentage=[]
		for lect in lectures:
			lect_count=0
			lect_cal=[0]*students.count()  #attendace of a lecture
			obj=Attendance.objects.filter(lecture=Lecture.objects.get(id=lect.id),date__range=[instance.fro,instance.to]).order_by("date")
			#print(obj)
			
			for date in obj:
				lect_session_count[lect_count]=lect_session_count[lect_count]+1
				total_session_count=total_session_count+1
				list_of_present=date.students_present.all()
				counter=0
				for stud in students:
					flag=1
					for stud_present in list_of_present:
						if stud.id==stud_present.id:
							flag=0
							lect_cal[counter]=lect_cal[counter]+1
							total_list[counter]=total_list[counter]+1
					counter=counter+1
			lect_count=lect_count+1
				
			listo.append(lect_cal)  #list of list of attendance
			lect_count=lect_count+1

		for x in total_list:
			if total_session_count==0:
				total_session_count=1
			percentage.append(round(((x/total_session_count)*100),2))

	lecto=section
	#print(listo)
	#print(total_list)
	#print(percentage)
	#problem in 
	context={"form":form,"stud":students,"presenty":listo,"cal":percentage,"model":lectures,"dont":my_id,"title":lecto,"form1":form1}
	return render(request,"section_viewer.html",context)







