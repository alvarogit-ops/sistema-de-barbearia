
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib import messages
from django.db import IntegrityError, transaction

from .models import Servico, Cliente, Agendamento


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
        elif User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
        else:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=nome,
                    )
                    Cliente.objects.create(usuario=user, telefone=telefone)
            except IntegrityError:
                messages.error(request, 'Não foi possível criar a conta. Tente novamente.')
            else:
                return redirect('login')

    return render(request, 'barber_grid/registro.html')


def agendamento(request, servico_id):
    servico = Servico.objects.get(id=servico_id)

    if request.method == "POST":
        data = request.POST.get("data")
        horario = request.POST.get("horario")

        cliente = Cliente.objects.get(usuario=request.user)

        Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            data=data,
            horario=horario
        )

        messages.success(request, "Agendamento feito com sucesso!")

        return redirect("historico_agendamentos")

    return render(
        request,
        "barber_grid/agendamento.html",
        {"servico": servico}
    )
    
def historico_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    context = {
        'agendamentos': agendamentos
    }
    return render(request, 'barber_grid/historico_agendamentos.html', context)