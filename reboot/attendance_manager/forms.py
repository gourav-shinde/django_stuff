from django import forms
from custom_user.models import User
from .models import To_fro,ulimit




class To_form(forms.ModelForm):

	class Meta:
		model=To_fro
		fields=("fro","to")
		labels={'fro':"From",'to':"To"}

class ulimit_form(forms.ModelForm):
	percentage=forms.IntegerField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
		}
		))
	class Meta:
		model=ulimit
		fields=("percentage",)
		labels={'percentage':"Percentage"}