from django.contrib import admin
from .models import MembroIabs, Parceiro, Reuniao
from .forms import MembroForms, ParceiroForms, ReuniaoForms

class MembroAdmin(admin.ModelAdmin):
	form = MembroForms

class ParceiroAdmin(admin.ModelAdmin):
	form = ParceiroForms

class ReuniaoAdmin(admin.ModelAdmin):
	form = ReuniaoForms

# Register your models here.
admin.site.register(MembroIabs, MembroAdmin)
admin.site.register(Parceiro, ParceiroAdmin)
admin.site.register(Reuniao, ReuniaoAdmin)
