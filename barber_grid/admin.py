from django.contrib import admin
<<<<<<< HEAD
from .models import Servico
# Register your models here.


=======
from .models import Agendamento, Cliente, Servico
# Register your models here.

admin.site.register(Agendamento)
admin.site.register(Cliente)
>>>>>>> main
admin.site.register(Servico)