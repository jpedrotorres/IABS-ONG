from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#Campos para atributos do tipo <select>
status_membro= [
	('A', 'Ativo'),
	('I', 'Inativo'),
	('F', 'Afastado')
]

status_parceiro= [
	('A', 'Ativo'),
	('I', 'Inativo')
]

status_reuniao= [
	('R', 'Realizada'),
	('A', 'Agendada'),
	('C', 'Cancelada')
]

tipo_membro= [
	('C', 'Colaborador'),
	('A', 'Administrador')
]

tipo_parceiro= [
	('PF', 'Pessoa Física'),
	('PJ', 'Pessoa Jurídica')
]

tipo_reuniao= [
	('P', 'Presencial'),
	('V', 'Virtual')
]

uf_estado = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins')
]

#Validações de dados com Regex
telefone_validator = RegexValidator(
    regex=r'^\d{10,11}$',
    message='O Telefone deve conter apenas números e ter 10 ou 11 dígitos.',
    code='telefone_invalido'
)

cep_validator = RegexValidator(
    regex=r'^\d{8}$',
    message='O CEP deve conter exatamente 8 números.',
    code='cep_invalido'
)

cpf_validator= RegexValidator(
    regex=r'^\d{11}$',
    message='O CPF deve conter 11 dígitos',
    code='cpf_invalido'
)

cnpj_validator= RegexValidator(
    regex=r'^\d{14}$',
    message='O CNPJ deve conter 14 dígitos',
    code='cnpj_invalido'
)

class MembroIabs(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    matricula= models.CharField(max_length=15, primary_key=True)
    tipo= models.CharField(max_length=1, choices=tipo_membro, default='C')
    nome= models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, validators=[cpf_validator])
    status= models.CharField(max_length=1, choices=status_membro, default='A')
    cargo= models.CharField(max_length=70, blank=True, null=True)
    email= models.EmailField(max_length=100, unique=True, blank=True)
    telefone= models.CharField(max_length=11, unique=True, blank=True, null=True, validators=[telefone_validator])
    data_nascimento= models.DateField(blank=True, null=True)

    def clean(self):
        if self.tipo == 'A' and not self.user:
            raise ValidationError({'user': 'O Usuário do Membro deve ser informado!'})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'A'

        if self.tipo == 'A' and self.user:
            self.nome = self.user.get_full_name() or self.user.username
            self.email = self.user.email

        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.nome

class Parceiro(models.Model):
    codigo = models.CharField(max_length=15, primary_key=True)
    tipo= models.CharField(max_length=2, choices=tipo_parceiro)
    nome= models.CharField(max_length=150, blank=True, null=True)
    razao_social= models.CharField(max_length=150, blank=True, null=True)
    cpf= models.CharField(max_length=11, unique=True, blank=True, null=True, validators=[cpf_validator])
    cnpj= models.CharField(max_length=14, unique=True, blank=True, null=True, validators=[cnpj_validator])
    status= models.CharField(max_length=1, choices=status_parceiro, default='A')
    nome_responsavel= models.CharField(max_length=150)
    cargo_responsavel= models.CharField(max_length=70, blank=True, null=True)
    email= models.EmailField(max_length=100, unique=True)
    telefone= models.CharField(max_length=11, unique=True, blank=True, null=True, validators=[telefone_validator])
    data_inicio= models.DateField(default=timezone.now)
    data_termino= models.DateField(blank=True, null=True)
    segmento= models.CharField(max_length=70, blank=True, null=True)
    uf= models.CharField(max_length=2, choices=uf_estado)
    cep= models.CharField(max_length=8, validators=[cep_validator])
    logradouro = models.CharField(max_length=200, blank=True, null=True)
    numero_local= models.CharField(max_length=15, blank=True, null=True)
    website= models.URLField(max_length=200, blank=True, null=True)
    rede_social= models.URLField(max_length=200, blank=True, null=True)
    contrato_parceria= models.FileField(upload_to='parceiro_contratos/', blank=True, null=True)
    observacoes= models.TextField(blank=True, null=True)

    def clean(self):
        if self.tipo == 'PF':
            if not self.nome:
                raise ValidationError({'nome':'O Parceiro deve ter Nome!'})
            if not self.cpf:
                raise ValidationError({'cpf':'O Parceiro deve ter CPF!'})

        if self.tipo == 'PJ':
            if not self.razao_social:
                raise ValidationError({'razao_social':'O Parceiro deve ter Razão Social!'})
            if not self.cnpj:
                raise ValidationError({'cnpj':'O Parceiro deve ter CNPJ!'})

        if self.nome and self.razao_social:
            raise ValidationError('O Parceiro não pode ter Nome e Razão Social simultaneamente!')

        if self.cpf and self.cnpj:
            raise ValidationError('O Parceiro não pode ter CPF e CNPJ simultaneamente!')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'A'

        super().save(*args, **kwargs)

    def __str__(self):
        if self.tipo == 'PF':
            return self.nome

        elif self.tipo == 'PJ':
            return self.razao_social

class Reuniao(models.Model):
    status= models.CharField(max_length=1, choices=status_reuniao, default='A')
    assunto= models.CharField(max_length=100)
    data_hora= models.DateTimeField(default=timezone.now)
    tipo= models.CharField(max_length=1, choices=tipo_reuniao)
    link_conferencia = models.URLField(max_length=200, blank=True, null=True)
    uf= models.CharField(max_length=2, choices=uf_estado, blank=True, null=True)
    cep= models.CharField(max_length=8, blank=True, null=True, validators=[cep_validator])
    logradouro = models.CharField(max_length=200, blank=True, null=True)
    numero_local= models.CharField(max_length=15, blank=True, null=True)
    relatorio= models.FileField(upload_to='reuniao_relatorios/', blank=True, null=True)
    membros= models.ManyToManyField(MembroIabs)
    parceiros= models.ForeignKey(Parceiro, on_delete=models.CASCADE)

    def clean(self):
        if self.tipo == 'V':
            if not self.link_conferencia:
                raise ValidationError({'link_conferencia':'A Reunião deve ter Link!'})

        if self.tipo == 'P':
            if not self.uf:
                raise ValidationError({'uf':'A UF da Reunião deve ser informada!'})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'A'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.assunto
