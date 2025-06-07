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

#Formulário base para os demais
class BaseForms(forms.ModelForms):
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


#Fomulário para Membro
class MembroForms(BaseForms):
	class Meta:
		model=MembroIabs
		fields="__all__"

#Formulário para Parceiro
class ParceiroForms(BaseForms):
	class Meta:
		model=Parceiro
		fields="__all__"

#Formulário para Reuniões
class ReuniaoForms(BaseForms):
	class Meta:
		model=Reuniao
		fields="__all__"

