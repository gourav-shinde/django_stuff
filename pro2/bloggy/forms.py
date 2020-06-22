from django import forms
from custom_user.models import User
from .models import Post
from app1.models import Section_class




class PostForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))

	description=forms.CharField(widget=forms.Textarea(attrs={
			'class':"form-control",'row':'3'
		}
		))

	class Meta:
		model=Post
		fields=('title','description')


class TeachPost(forms.ModelForm):
		section=forms.ModelChoiceField(queryset=Section_class.objects.all(), empty_label="(Select Class)",
		widget=forms.Select(
		attrs={
			'class':"form-control",
		}
		)
		)
		title=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))
		description=forms.CharField(widget=forms.Textarea(attrs={
			'class':"form-control",'row':'3'
		}
		))
		class Meta:
			model=Post
			fields=('section','title','description')

