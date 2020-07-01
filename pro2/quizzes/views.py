from django.shortcuts import render,redirect
from .models import (Quiz,Question,Answer,QuizTaker,UsersAnswer)
from app1.models import (Students,Lecture,Attendance,Section_class)
from .forms import (Quiz_form,Answer_form)

#form images
from django.core.files.storage import FileSystemStorage

# Create your views here.
def quiz_view(request):
	return render(request,"quiz_home.html",{})

def createquiz_view(request):
	lecture=Lecture.objects.filter(user=request.user)
	if request.POST:
			form=Quiz_form(request.POST or None)
			if form.is_valid():
				instance=form.save()
				print(instance.id)
				ret="/quiz/question/"+str(instance.slug)+"/1"
				return redirect(ret)
	else:
		form=Quiz_form(None)
		form.fields['lecture'].queryset = lecture

	context={'form':form,'title':"Quiz"}
	return render(request,"create_quiz.html",context)

def question_view(request,my_id,num=0):
	print(request.POST)
	if request.POST:
		quiz=Quiz.objects.get(slug=my_id)
		que=Question(quiz=quiz,label=request.POST.get('question'),img=request.FILES.get('qimg'),order=num)
		que.save()
		print(que)
		imglist=request.POST.getlist('optimage')
		
		
		
		
		optno=request.POST.get('correct')
		optno=optno[0]
		options=request.POST.getlist('option')
		print(options)
		
			
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
			ret="/quiz/question/"+str(my_id)+"/"+str(num)
			return redirect(ret)
		else:
			return redirect("quizzes:quizy")



	context={'num':num}
	return render(request,"create_question.html",context)
