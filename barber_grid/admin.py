from django.contrib import admin
from .models import Servico, HorariodeFuncionamento, BloqueioHorario
# Register your models here.

admin.site.register(Servico)
admin.site.register(HorariodeFuncionamento)
admin.site.register(BloqueioHorario)