
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib import messages
from .models import Servico, Cliente, Agendamento


def setup(request):
    return render(request, 'barber_grid/setup.html')

def pagina_servicos(request):
    servicos = Servico.objects.all()
    context = {
        'servicos': servicos
    }

    return render(request, 'barber_grid/pagina_servicos.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("senha")
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            auth_login(request, user)
            return redirect('pagina_servicos')
        else:
            messages.error(request, 'Usuário / senha inválidos')
            

    return render(request, 'barber_grid/login.html')

def registro(request):
    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        telefone = (request.POST.get("telefone") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("senha") or ""

        if not nome or not telefone or not email or not password:
            messages.error(request, 'Preencha todos os campos.')
        else:
                return redirect('login')

    return render(request, 'barber_grid/registro.html')
