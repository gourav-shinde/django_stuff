from django.shortcuts import render,redirect
from custom_user.forms import Register_Form,AccountAuthForm,AccountUpdateForm,Registernew_Form
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import User

#for verification
from django.urls import reverse
from django.core.mail import EmailMessage
from .utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
import threading

# Create your views here.
class EmailThread(threading.Thread):

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=True)

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
			user=form.save(commit=False)
			user.is_active=False
			if user.is_student==False:
				user.is_teacher=True
			user.save()
			#domain,relative url,token,uid
			user=user
			domain=get_current_site(request).domain
			uidb64=urlsafe_base64_encode(force_bytes(user.id)).decode()
			token= account_activation_token.make_token(user)
			link=reverse('custom_user:activate',kwargs={'uidb64':uidb64,'token':token})
			activate_url="https://"+domain+link
			
			subject="Email verification"
			message="Hi "+str(user.username)+"\n"+str(activate_url)+"\nIgnore(if not used arsenalG)"
			to_list=[user.email]
			email = EmailMessage(
										subject,
										message,
										'gauravshinde696969@gmail.com',
										to_list
									)
			EmailThread(email).start()
			#send_mail(subject,message,"gauravshinde696969@gmail",to_list,fail_silently=True)
			return redirect('custom_user:wait')
		else:
			context={'registeration_form':form}
	else:
		
		form=Registernew_Form()
		context["registeration_form"]=form
	return render(request,'registernew.html',context)


def verification(request,uidb64,token):

	id = force_text(urlsafe_base64_decode(uidb64).decode())
	user = User.objects.get(id=id)
	if not account_activation_token.check_token(user, token):
		return redirect('custom_user:login')
	if user.is_active:
		return redirect('custom_user:login')
	user.is_active = True
	user.save()
		

	

	return redirect('custom_user:login')



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
			if not instance.is_active:
				return redirect("custom_user:wait")
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
		return redirect("custom_user:login")

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


def wait(request):
	return render(request,"waiting.html",{})


def passy(request):
	error=""
	if request.POST:
		passy=request.POST.get('pass')
		if passy=="3691215":
			return redirect("custom_user:register")
		else:
			error="invalid password"
	return render(request,"pass.html",{'error':error})

