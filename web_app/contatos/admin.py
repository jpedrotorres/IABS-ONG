from django.contrib import admin
from .models import MembroONG
from .models import Parceiro
from .models import Reuniao
from .models import ParticipacaoMembro

# Register your models here.
admin.site.register(MembroONG)
admin.site.register(Parceiro)
admin.site.register(Reuniao)
admin.site.register(ParticipacaoMembro)
