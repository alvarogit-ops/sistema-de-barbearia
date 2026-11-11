from django.contrib import admin
from .models import Servico, HorariodeFuncionamento, BloqueioHorario, Cliente
# Register your models here.

admin.site.register(Servico)
admin.site.register(HorariodeFuncionamento)
admin.site.register(BloqueioHorario)
admin.site.register(Cliente)