from django.shortcuts import render
from .models import Agendamento


def index(request):
    return render(request, 'barber_grid/index.html')


def agendamento(request):

    agendamento = Agendamento.objects.order_by('data_agendada')

    context = {'agendamentos': agendamento}
    return render(request, 'barber_grid/agendamento.html', context)