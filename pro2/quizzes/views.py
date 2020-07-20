from django.shortcuts import render,redirect,get_object_or_404
from .models import (Quiz,Question,Answer,QuizTaker,UsersAnswer)
from app1.models import (Students,Lecture,Attendance,Section_class)
from .forms import (Quiz_form,Answer_form)
from custom_user.models import User
from django.http import JsonResponse
from django.forms.models import model_to_dict


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
def quiz_view(request):
	lecture=Lecture.objects.filter(user=request.user)
	quiz=[]
	for lec in lecture:
		q=Quiz.objects.filter(lecture=lec)
		for x in q:
			quiz.append(x)
	if request.POST:
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


	return render(request,"viewww.html",{'quiz':quiz,'form':form,'title':"Quiz"})


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


def quiz_detail_view(request,my_id):
	quiz=Quiz.objects.get(slug=my_id)
	print(quiz)
	questions=Question.objects.filter(quiz=quiz).order_by('order')
	print(questions)
	view_list=[]
	for q in questions:
		ans=Answer.objects.filter(question=q)
		list1={'q':q,'ans':ans}
		view_list.append(list1)
		print(list1)

	print(view_list)
	context={'listo':view_list,'quiz':quiz}
	return render(request,"quiz_view.html",context)


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




#######student side viewsssssss


def quiz_stud(request):
	quizzes=QuizTaker.objects.filter(user=request.user).order_by('quiz__roll_out_time')
	quiz=quizzes.filter(completed=False)
	quiz_completed=quizzes.filter(completed=True)
	context={'quiz':quiz,'completed':quiz_completed}
	return render(request,"stud_quizview.html",context)

def quiz_trans(request,my_id):
	quiz_instance=Quiz.objects.get(slug=my_id)
	context={'q':quiz_instance}
	return render(request,'exam/start.html',context)

def quiz_back(request,my_id):
	quiz_instance=Quiz.objects.get(slug=my_id)
	context={'q':quiz_instance}
	return render(request,'exam/quiz.html',context)

def quiz_dock(request,my_id):
	quiz_instance=Quiz.objects.get(slug=my_id)
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

	context={
	}
	return render(request,"exam/end.html",context)

