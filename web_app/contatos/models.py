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

tipo_parceiro= [
    ("PF", "Pessoa Física")
    ("PJ", "Pessoa Jurídica")
]

uf_estado = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins")
]

tipo_reuniao= [
    ("P", "Presencial")
    ("V", "Virtual")
]

# Revisar
class MembroIabs(models.Model):
    matricula= models.CharField(max_length=15, primary_key=True)
    tipo= models.CharField(max_length=1, choices=tipo_membro, default="C", blank=True)
    nome= models.CharField(max_length=150, blank=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True)
    status= models.CharField(max_length=1, choices=status_membro, default="A", blank=True)
    cargo= models.CharField(max_length=70, blank=True, null=True)
    email= models.EmailField(max_length=100, unique=True, blank=True)
    telefone_celular= models.IntegerField(max_length=11, unique=True, blank=True, null=True)
    # declarar: data_nascimento (blank=True, null=True)

    def __str__(self):
        return self.nome
	
	# verificar: tipo, nome, cpf, status, email

class Usuario(models.Model):
    nome= models.CharField(max_length=20, primary_key=True)
    senha= models.CharField(max_length=15, blank=True)
    membro_adm= models.OneToOneField(MembroIabs, on_delete=models.CASCADE)

# Revisar
class Parceiro(models.Model):
    codigo = models.CharField(max_length=15, primary_key=True)
    tipo= models.CharField(max_length=2, choices=tipo_parceiro, blank=True)
    nome= models.CharField(max_length=150, blank=True, null=True)
    razao_social= models.CharField(max_length=150, blank=True, null=True)
    cpf= models.CharField(max_length=11, unique=True, blank=True, null=True)
    cnpj= models.CharField(max_length=14, unique=True, blank=True, null=True)
    status= models.CharField(max_length=1, choices=status_parceiro, default="A", blank=True)
    nome_responsavel= models.CharField(max_length=150, blank=True)
    cargo_responsavel= models.CharField(max_length=70, blank=True, null=True)
    email= models.EmailField(max_length=100, unique=True, blank=True)
    telefone_fixo= models.IntegerField(max_length=10, unique=True, blank=True, null=True)
    data_inicio= models.DateField(default=timezone.now, blank=True)
    # declarar: data_termino= (blank=True, null=True)
    segmento= models.CharField(max_length=70, blank=True, null=True)
    # uf= models.CharField(max_length=2, choices=uf_estado, blank=True)
    # cep= models.IntegerField(max_length=8, blank=True)
    # declarar: logradouro
    # OU utilizar de classe Endereço
    website= models.URLField(max_length=200, blank=True, null=True)
    rede_social= models.URLField(max_length=200, blank=True, null=True)
    # declarar: contrato_parceria= models.ArchiveField ? (blank=True, null=True)
    observacoes= models.TextField(blank=True, null=True)

    def __str__(self):
        if self.tipo == "PF":
            return self.nome
        elif self.tipo == "PJ":
            return self.razao_social
        else:
            # lançar erro
        
    # verificar: tipo, nome/razao_social, cpf/cnpj, status, email, data_inicio, uf/cep/logradouro ou endereço

# Revisar
class Reuniao(models.Model):
    codigo= models.CharField(max_length=15, primary_key=True)
    status= models.CharField(max_length=1, choices=status_reuniao, default="A", blank=True)
    assunto= models.CharField(max_length=100, blank=True)
    data_hora= models.DateTimeField(default=timezone.now, blank=True)
    tipo= models.CharField(max_length=1, choices=tipo_reuniao, blank=True)
    # Se tipo == V
    link_conferencia = models.URLField(max_length=200, blank=True, null=True)
    # Se tipo == P
    # uf= models.CharField(max_length=2, choices=uf_estado, blank=True, null=True)
    # cep= models.IntegerField(max_length=8, blank=True, null=True)
    # declarar: logradouro (blank=True, null=True)
    # OU utilizar de classe Endereço
    
    # declarar: relatorio= models.ArchiveField ? (blank=True, null=True)
    membros= models.ManyToManyField(MembroIabs)
    parceiros= models.ForeignKey(Parceiro, on_delete=models.CASCADE)

    def __str__(self):
        return self.assunto

    # verificar: status, assunto, data_hora, tipo, link_conferencia, uf/cep/logradouro ou endereço