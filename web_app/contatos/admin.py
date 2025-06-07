from django.contrib import admin
from .models import MembroIabs
from .models import Parceiro
from .models import Reuniao

# Register your models here.
admin.site.register(MembroIabs)
admin.site.register(Parceiro)
admin.site.register(Reuniao)
