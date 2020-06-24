from django.shortcuts import render,redirect
from custom_user.forms import Register_Form,AccountAuthForm,AccountUpdateForm,Registernew_Form
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import User
# Create your views here.

def registeration_view(request):
	context={}
	if request.POST:
		form=Register_Form(request.POST)
		if form.is_valid():
			form.save()
			email=form.cleaned_data.get('email')
			raw_password=form.cleaned_data.get('password1')
			account=authenticate(email=email,password=raw_password)
			login(request,account)
			return redirect('root')
		else:
			context["registeration_form"]=form
	else:
		form=Register_Form()
		context["registeration_form"]=form
	return render(request,'register.html',context)	

def newregister(request):
	context={}
	if request.POST:
		form=Registernew_Form(request.POST)
		if form.is_valid():
			form.save()
			email=form.cleaned_data.get('email')
			raw_password=form.cleaned_data.get('password1')
			account=authenticate(email=email,password=raw_password)
			login(request,account)
			return redirect('root')
		else:
			error="Email already registered/password validation"
			context={'registeration_form':form,'error':error}
	else:
		
		form=Registernew_Form()
		context["registeration_form"]=form
		context["error"]=""
	return render(request,'registernew.html',context)



def logout_view(request):
	logout(request)
	return redirect("root")


def login_view(request):  #login 
	context={}
	user=request.user

	if user.is_authenticated:
		return redirect("root")

	if request.POST:
		form=AccountAuthForm(request.POST)
		if form.is_valid():
			email=request.POST['email']
			password=request.POST['password']
			user=authenticate(email=email,password=password)

			if user:
				login(request,user)
				instance=request.user
				if instance.is_student:
					return redirect("app1:studprof")
				if instance.is_teacher:
					return redirect("app1:lectures")
				else:
					return redirect("root")
	else:
		form=AccountAuthForm()

	context['login_form']=form
	return render(request,'login.html',context)


def student_loginview(request):
	error=""
	user=request.user
	print(request.POST)
	if request.POST:
		email=request.POST.get('email')
		password=request.POST.get('pass')
		user=authenticate(email=email,password=password)

		if user:
			login(request,user)
			instance=request.user
			if instance.is_student:
				return redirect("app1:studprof")
			if instance.is_teacher:
				return redirect("app1:lectures")
			else:
				return redirect("root")
		else:
			error="Invalid Credentials"
	
	context={'error':error}
	return render(request,'student_login.html',context)



def account_view(request):

	if not request.user.is_authenticated:
		return redirect("login")

	context={}

	if request.POST:
		form=AccountUpdateForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
	else:
		form=AccountUpdateForm(
			initial={
			'email':request.user.email,
			"username":request.user.username,
			})
	context['account_form']=form
	return render(request,"account.html",context)

