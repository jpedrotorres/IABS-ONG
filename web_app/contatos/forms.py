from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

#create forms here
#Formulário de Login
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

#Formulário para Parceiro
class ParceiroForms(forms.ModelForm):
	class Meta:
		model=MembroIabs
		fields="__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.instance.pk:
			self.fields.pop("status")

	def save(self, commit=True):
		instance = super().save(commit=False)

		if not instance.pk:
			instance.status = "A"

		if commit:
			instance.save()

		return instance

