
from django.shortcuts import render
from .models import Servico
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages

def setup(request):
    return render(request, 'barber_grid/setup.html')

def pagina_servicos(request):
    servicos = Servico.objects.all()
    context = {
        'servicos': servicos
    }

    return render(request, 'barber_grid/pagina_servicos.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("senha")
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('pagina_servicos')
        else:
            messages.error(request, 'Usuário / senha inválidos')
            

    return render(request, 'barber_grid/login.html')

def registro(request):
    return render(request, 'barber_grid/registro.html')
