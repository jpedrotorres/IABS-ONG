from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import MembroIabs, Parceiro, Reuniao

#create forms here
tipo_membro= [
	('C', 'Colaborador'),
	('A', 'Administrador')
]



tipo_reuniao= [
	('P', 'Presencial'),
	('V', 'Virtual')
]

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
class BaseForms(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs.update({
				"class": "info-page-input"
			})

		if not self.instance.pk and 'status' in self.fields:
			self.fields["status"].widget = forms.HiddenInput()

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
		widgets = {
			"tipo": forms.RadioSelect,
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['status'].widget.attrs.update({'class': 'status-input-info'})

		self.order_fields([
		"matricula",
		"nome",
		"cpf",
		"status",
		"cargo",
		"email",
		"telefone",
		"data_nascimento",
		"tipo",
		"user"
		])

#Formulário para Parceiro
class ParceiroForms(BaseForms):
	tipo_parceiro= [
		('PF', 'Pessoa Física'),
		('PJ', 'Pessoa Jurídica')
	]

	tipo = forms.ChoiceField(
		choices=tipo_parceiro,
		widget=forms.RadioSelect(
			attrs={'class': 'form-check-input'},
		),
		required=True
	)

	class Meta:
		model=Parceiro
		fields="__all__"
		widgets = {
			"tipo": forms.RadioSelect,
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.order_fields([
		"codigo",
		"status",
		"nome",
		"cpf",
		"razao_social",
		"cnpj",
		"nome_responsavel",
		"cargo_responsavel",
		"email",
		"uf",
		"cep",
		"logradouro",
		"numero_local",
		"observacoes",
		"contrato_parceria",
		"tipo",
		"segmento",
		"website",
		"telefone",
		"rede_social",
		"data_inicio",
		"data_fim",
		])

#Formulário para Reuniões
class ReuniaoForms(BaseForms):
	class Meta:
		model=Reuniao
		fields="__all__"


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['tipo'].empty_label = None

		self.order_fields([
		"assunto",
		"parceiros",
		"membros",
		"status",
		"tipo",
		"uf",
		"cep",
		"logradouro",
		"numero_local",
		"link_conferencia",
		"data_hora",
		])
