from django.shortcuts import render,redirect,get_object_or_404
from .models import (Quiz,Question,Answer,QuizTaker,UsersAnswer,Quiz_point)
from app1.models import (Students,Lecture,Attendance,Section_class)
from .forms import (Quiz_form,Answer_form)
from custom_user.models import User
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required


#encoder/decoder
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError


#form images
from django.core.files.storage import FileSystemStorage


def make_quiz_models(instance):
	students=Students.objects.filter(section=instance.lecture.section_class)
	for x in students:
		try:
			user=User.objects.get(email=x.email)
			if user.is_student:
				model=QuizTaker(user=user,quiz=instance)
				print("created")
				model.save()
				print("saved")
		except:
			pass
		

	

# Create your views here.

@login_required(login_url='/account/login')
def quiz_view(request):
	now = datetime.datetime.now()
	lecture=Lecture.objects.filter(user=request.user)
	quiz=Quiz.objects.filter(lecture__in=lecture)
	
	quiz_expired=quiz.filter(stop_time__lte=now)
	quiz_active=quiz.filter(stop_time__gt=now)
	error=[]
	success=[]
	if request.POST:
			if request.POST.get('share_id'):
				id=request.POST.get('share_id')
				try:
					id=force_text(urlsafe_base64_decode(id).decode())
					id=int(id)-1009
					try:
						quiz=Quiz.objects.get(id=id)
						lect_selected=request.POST.get('lecture')
						lect_selected=Lecture.objects.get(id=int(lect_selected))
						#print(lect_selected)
						quiz_start=Quiz(lecture=lect_selected,name=request.POST.get('Name'),description=quiz.description,roll_out_time=quiz.roll_out_time,stop_time=quiz.stop_time,pointer=True)
						quiz_start.save()
						relate_quiz=Quiz_point(quiz_fro=quiz_start,quiz_to=quiz)
						relate_quiz.save()
						##########################create student objects
						make_quiz_models(quiz_start)
						return redirect("quizzes:quizy")
						success.append('Quiz Imported Successfully')
					except:
						error.append("Quiz does not exist")
				except :
					error.append("No such ID")
					
				
				#print(id)
				
					
				
			
			form=Quiz_form(request.POST or None)
			if form.is_valid():
				instance=form.save()
				print(instance.id)
				##########################create student objects
				make_quiz_models(instance)
				ret="/quiz/question/"+str(instance.slug)+"/1/0"
				return redirect(ret)
	else:
		form=Quiz_form(None)
		form.fields['lecture'].queryset = lecture
	context={'quiz':quiz_active,'lecture':lecture,'quiz_e':quiz_expired,'form':form,'title':"Quiz",'error':error,'success':success}

	return render(request,"viewww.html",context)

@login_required(login_url='/account/login')
def createquiz_view(request):
	lecture=Lecture.objects.filter(user=request.user)
	if request.POST:
			form=Quiz_form(request.POST or None)
			if form.is_valid():
				instance=form.save()
				print(instance.id)
				ret="/quiz/question/"+str(instance.slug)+"/1/0"
				return redirect(ret)
	else:
		form=Quiz_form(None)
		form.fields['lecture'].queryset = lecture

	context={'form':form,'title':"Quiz"}
	return render(request,"create_quiz.html",context)

@login_required(login_url='/account/login')
def question_view(request,my_id,num=0,flag=0):
	print(request.POST)
	relay=0
	if request.POST:
		quiz=Quiz.objects.get(slug=my_id)
		if flag==1:
			questions=Question.objects.filter(quiz=quiz).order_by('order')
			count=questions.count()
			if count:
				if not questions[count-1]==(count):
					num=count+1
					que=Question(quiz=quiz,label=request.POST.get('question'),img1=request.FILES.get('qimg'),order=num)
					que.save()
					relay=1
				else:	
					for i in range(0,count):
						if not int(i+1)==int(questions[i].order):
							que=Question(quiz=quiz,label=request.POST.get('question'),img1=request.FILES.get('qimg'),order=i+1)
							que.save()
							num=i+1
							break
			else:
				que=Question(quiz=quiz,label=request.POST.get('question'),img1=request.FILES.get('qimg'),order=num)
				que.save()
				relay=1

		else:
			que=Question(quiz=quiz,label=request.POST.get('question'),img1=request.FILES.get('qimg'),order=num)
			que.save()
		imglist=request.POST.getlist('optimage')
		
		
		
		
		optno=request.POST.get('correct')
		optno=optno[0]
		options=request.POST.getlist('option')
		
			
		count=0
		
		
		for op in options:
			print(op)
			print(request.FILES.get(str(count)))
			
			if count+1==int(optno):
				ans=Answer(question=que,label=op,img=request.FILES.get(str(count+1)),is_correct=True)
			else:
				ans=Answer(question=que,img=request.FILES.get(str(count+1)),label=op)
				
			
			ans.save()


			count=count+1
		if request.POST.get('next'):
			num=num+1
			if relay:
				ret="/quiz/question/"+str(my_id)+"/"+str(num)+"/0"
			else:
				ret="/quiz/question/"+str(my_id)+"/"+str(num)+"/"+str(flag)
			return redirect(ret)
		else:
			return redirect("quizzes:quizy")



	context={'num':num}
	return render(request,"create_question.html",context)

@login_required(login_url='/account/login')
def quiz_detail_view(request,my_id):
	quiz=Quiz.objects.get(slug=my_id)
	quiz1=quiz
	if quiz.pointer:
		relate=Quiz_point.objects.get(quiz_fro=quiz)
		quiz1=Quiz.objects.get(id=relate.quiz_to.id)
	quiz_id=urlsafe_base64_encode(force_bytes(quiz.id+1009)).decode()
	#print(quiz)
	questions=Question.objects.filter(quiz=quiz1).order_by('order')
	print(questions)
	view_list=[]
	for q in questions:
		ans=Answer.objects.filter(question=q)
		list1={'q':q,'ans':ans}
		view_list.append(list1)
		print(list1)

	print(view_list)
	context={'listo':view_list,'quiz':quiz,'share_id':quiz_id,'editable':quiz.pointer}
	return render(request,"quiz_view.html",context)



@login_required(login_url='/account/login')
def quiz_delete(request,my_id):
	obj=get_object_or_404(Quiz,slug=my_id)
	print(my_id)
	if request.POST:
		obj.delete()
		return redirect("quizzes:quizy")
	context={
	"object":obj
	}
	return render(request,"delete.html",context)

@login_required(login_url='/account/login')
def question_delete(request,my_id,num):
	obj=get_object_or_404(Question,id=num)
	print(my_id)
	if request.POST:
		obj.delete()
		ret="/quiz/view/"+my_id
		return redirect(ret)
	context={
	"object":obj
	}
	return render(request,"delete.html",context)

@login_required(login_url='/account/login')
def quiz_edit(request,my_id):
	obj=get_object_or_404(Quiz,slug=my_id)
	form=Quiz_form(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		ret="/quiz/view/"+str(my_id)
		return redirect(ret)
	context={
	"form":form,"title":obj
	}
	return render(request,"forms.html",context)

@login_required(login_url='/account/login')
def score_view(request,my_id):
	quiz_takers=QuizTaker.objects.filter(quiz__slug=my_id,completed=True)
	emails=[]
	for x in quiz_takers:
		emails.append(x.user.email)
	quiz=Quiz.objects.get(slug=my_id)
	section=Section_class.objects.get(id=quiz.lecture.section_class.id)
	students=Students.objects.filter(section=section,email__in=emails)
	quiz_takers=zip(quiz_takers,students)
	context={'result':quiz_takers,'quiz':quiz}
	return render(request,'scores.html',context)




#######student side viewsssssss


def quiz_stud(request):
	quizzes=QuizTaker.objects.filter(user=request.user).order_by('quiz__roll_out_time')
	now = datetime.datetime.now()
	print(now)
	quiz=quizzes.filter(completed=False,quiz__stop_time__gte=now)
	quiz_completed=quizzes.filter(Q(completed=True)|Q(quiz__stop_time__lte=now))
	context={'quiz':quiz,'completed':quiz_completed}
	return render(request,"stud_quizview.html",context)

def quiz_trans(request,my_id):
	quiz_instance=Quiz.objects.get(slug=my_id)
	now = timezone.now()
	if quiz_instance.roll_out_time>now:
		return redirect("quizzes:quiz_stud")
	context={'q':quiz_instance}
	return render(request,'exam/start.html',context)

def quiz_back(request,my_id):
	quiz_instance=Quiz.objects.get(slug=my_id)
	context={'q':quiz_instance}
	return render(request,'exam/quiz.html',context)

def quiz_dock(request,my_id):
	quiz_instance=Quiz.objects.get(slug=my_id)
	if quiz_instance.pointer:
		relate=Quiz_point.objects.get(quiz_fro=quiz_instance)
		quiz_instance=Quiz.objects.get(id=relate.quiz_to.id)
	questions=Question.objects.filter(quiz=quiz_instance).order_by('order')
	json_list=[]
	for q in questions:
		ans=Answer.objects.filter(question=q)
		a_list=[]
		for a in ans:
			if a.is_correct:
				answer=a.label
			a_list.append(a.label)

		list1={'id':q.order,'question':q.label,'answer':answer,'options':a_list}
		json_list.append(list1)
	


	
	data={'quiz_list':json_list}
	return JsonResponse(data)

def quiz_end(request,my_id,score):
	quiz_taker=QuizTaker.objects.get(quiz__slug=my_id,user=request.user)
	print(score)
	quiz_taker.completed=True
	quiz_taker.score=score
	quiz_taker.save()

	context={
	}
	return render(request,"exam/end.html",context)

