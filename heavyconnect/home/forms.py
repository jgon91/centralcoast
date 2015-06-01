from django import forms
from django.contrib.auth.models import User

class loginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)