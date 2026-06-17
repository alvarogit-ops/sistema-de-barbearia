from django.shortcuts import render
from .models import Agendamento
from .forms import ClientesForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'barber_grid/index.html')


def agendamento(request):

    agendamento = Agendamento.objects.order_by('data_agendada')

    context = {'agendamentos': agendamento}
    return render(request, 'barber_grid/agendamento.html', context)

def cadastro_clientes(request):
    if request.method != 'POST':
        form = ClientesForm()
    else:
        form = ClientesForm(request.POST)
          #validar campos válidos:
        if form.is_valid():
           form.save()
		  #reverse utiliza name pra trazer a página
           return HttpResponseRedirect(reverse('agendamento'))

    context = {'form': form}
    return render(request, 'barber_grid/cadastro_clientes.html', context)

