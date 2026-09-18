from django.shortcuts import render
from .models import Servico

def setup(request):
    return render(request, 'barber_grid/setup.html')

def pagina_servicos(request):
    servicos = Servico.objects.all()
    context = {
        'serviços': servicos
    }
    return render(request, 'barber_grid/pagina_servicos.html', context)



