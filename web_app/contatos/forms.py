from django import forms
from django.contrib.auth.forms import AuthenticationForm

#create forms here

class MembroLoginForms(AuthenticationForm):
	username= forms.CharField(widget=forms.TextInput(attrs={"class": "input-login", "placeholder": "nome de usuário"}))
	password= forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-login", "placeholder": "senha"}))
