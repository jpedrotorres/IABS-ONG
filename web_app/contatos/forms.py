from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

#create forms here

class MembroLoginForms(AuthenticationForm):
	error_messages= {
		"invalid_login": _("usuário ou senha inválidos!"),
		"inactive": _("essa conta está inativa")
	}

	username= forms.CharField(
		label="usuário:",
		widget=forms.TextInput(attrs={"class": "input-login", "placeholder": "nome de usuário"})
	)
	password= forms.CharField(
		label="senha:",
		widget=forms.PasswordInput(attrs={"class": "input-login", "placeholder": "senha"})
	)
