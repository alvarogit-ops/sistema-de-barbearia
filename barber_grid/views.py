from django.shortcuts import render
from django.http import HttpResponse
from .models import Agendamento
# Create your views here.

def index(request):
    agendamento = Agendamento.objects.all()
    context = {'agendamentos': agendamento}
    return render(request, 'barber_grid/agendamento.html', context)