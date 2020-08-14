from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from custom_user.models import User


class Register_Form(UserCreationForm):
	email=forms.EmailField(max_length=50,widget=forms.TextInput(
		attrs={
			'class':"form-control"
		}
		))
	username=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control"
		}
		))
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(
		attrs={
			'class':"form-control"
		}
		))

	password2=forms.CharField(label="Password-confirmation",widget=forms.PasswordInput(
		attrs={
			'class':"form-control"
		}
		))

	class Meta:
		model=User
		fields=("username","email","password1","password2","is_student","is_teacher")


class Registernew_Form(UserCreationForm):
	email=forms.EmailField(max_length=50,widget=forms.TextInput(
		attrs={
			'class':"formy",'placeholder':'Email'
		}
		))
	username=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"formy",'placeholder':'Username'
		}
		))
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(
		attrs={
			'class':"formy",'placeholder':'Password'
		}
		))

	password2=forms.CharField(label="Password-confirmation",widget=forms.PasswordInput(
		attrs={
			'class':"formy",'placeholder':'Repeat Your Password'
		}
		))

	is_student=forms.BooleanField(required=False,widget=forms.CheckboxInput(
		attrs={
			'class':"agree-term",'id':'agree-term','name':'agree-term'
		}
		))
	class Meta:
		model=User
		fields=("username","email","password1","password2","is_student")



class AccountAuthForm(forms.ModelForm):
	email=forms.EmailField(max_length=50,widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))
	password=forms.CharField(label="Password",widget=forms.PasswordInput(
		attrs={
			'class':"form-control",
		}
		))

	class Meta:
		model=User
		fields=['email','password']

	def clean(self):
		if self.is_valid():
			email=self.cleaned_data['email']
			password=self.cleaned_data['password']

			if not authenticate(email=email,password=password):
				raise forms.ValidationError("Invalid Login")




class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model=User
		fields=('email','username')

	def clean_email(self):
		if self.is_valid():
			email=self.cleaned_data['email']
			try:
				account=User.objects.exclude(pk=self.instance.pk).get(email=email)
			except User.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.'%account)


	def clean_username(self):
		if self.is_valid():
			username=self.cleaned_data['username']
			try:
				account=User.objects.exclude(pk=self.instance.pk).get(username=username)
			except User.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.'%account.username)



