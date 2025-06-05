from django.db import models
from django.utils import timezone

status_membro= [
	("A", "Ativo"),
	("I", "Inativo"),
	("F", "Afastado")
]

status_parceiro= [
	("A", "Ativo"),
	("I", "Inativo")
]

status_reuniao= [
	("R", "Realizada"),
	("A", "Agendada"),
	("C", "Cancelada")
]

tipo_membro= [
	("C", "Colaborador")
	("A", "Administrador")
]

# Revisar
class  MembroONG(models.Model):
	matricula= models.CharField(primary_key=True)
	nome= models.CharField(max_length=100, blank=True)
	cpf = models.CharField(max_length=11, blank=True)
	cargo= models.CharField(max_length=70, blank=True, null=True)
	email= models.EmailField(max_length=100, unique=True, blank=True)
	status= models.CharField(max_length=1, choices=status_membro, default="A", blank=True)
	telefone_celular= models.IntegerField(max_length=11, blank=True, null=True)
	# declarar: data_nascimento (blank=True, null=True)
	tipo= models.CharField(max_length=1, choices=tipo_membro, default="C", blank=True)

	def __str__(self):
		return self.nome
	
	# verificar: nome, cpf, email, status, tipo

class  Parceiro(models.Model):
	nome= models.CharField(max_length=255)
	responsavel_parceiro= models.CharField(max_length=255)
	cargo_responsavel_parceiro= models.CharField(max_length=100)
	status= models.CharField(max_length=1, choices=status_parceiro, default="A")
	tipo_parceiro= models.CharField(max_length=100)
	cpf= models.CharField(max_length=11, null=True)
	cnpj= models.CharField(max_length=14, null=True)
	endereco= models.CharField(max_length=255)
	email= models.EmailField(max_length=100)
	telefone= models.CharField(max_length=20)
	data_inicio= models.DateField(default=timezone.now)
	area_interesse= models.CharField(max_length=255)
	website= models.URLField(max_length=200)
	contrato_parceiro= models.CharField(max_length=255)
	observacoes= models.TextField(blank=True)
	membroONG= models.ForeignKey(MembroONG, on_delete=models.CASCADE)

	def __str__(self):
		return self.nome

class  Reuniao(models.Model):
	data_hora= models.DateTimeField(default=timezone.now)
	assunto= models.CharField(max_length=100)
	tipo_reuniao= models.CharField(max_length=100)
	local= models.CharField(max_length=255)
	status= models.CharField(max_length=1, choices=status_reuniao, default="A")
	participantes= models.TextField()
	relatorio= models.CharField(max_length=200)
	parceiros= models.ForeignKey(Parceiro, on_delete=models.CASCADE)

	def __str__(self):
		return self.assunto

class  ParticipacaoMembro(models.Model):
	reuniao= models.ForeignKey(Reuniao, on_delete=models.CASCADE)
	membrosONG= models.ForeignKey(MembroONG, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.reuniao}, {self.membrosONG}"
