from django.contrib import admin
from .models import Agendamento, Cliente, Servico
# Register your models here.

admin.site.register(Agendamento)
admin.site.register(Cliente)
admin.site.register(Servico)