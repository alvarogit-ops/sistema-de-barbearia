
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

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("senha")
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            auth_login(request, user)

            if user.is_staff:
                return redirect('historico_agendamentos')
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

    return render(request, 'barber_grid/registro.html')


def agendamento(request, servico_id):
    servico = Servico.objects.get(id=servico_id)

    if request.method == "POST":
        data = request.POST.get("data")
        horario = request.POST.get("horario")

        cliente = Cliente.objects.get(usuario=request.user)

        if Agendamento.objects.filter(
            cliente=cliente,
            servico=servico,
            data=data,
            horario=horario
        ).exists():

            messages.error(
                request,
                "Este horário já está agendado."
            )

            return redirect(
                "agendamento",
                servico_id=servico_id
            )

        Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            data=data,
            horario=horario
        )

        messages.success(
            request,
            "Agendamento feito com sucesso!"
        )

        return redirect("usuario_historico")

    return render(
        request,
        "barber_grid/agendamento.html",
        {"servico": servico}
    )


def historico_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    context = {
        'agendamentos': agendamentos,
    }
    return render(request, 'barber_grid/historico_agendamentos.html', context)


def painel_admin(request):
    return render(request, 'barber_grid/painel_admin.html')

def servico(request):
    if request.method == "POST":
        nome_servico = request.POST.get("nome_servico")
        preco = request.POST.get("preco")
        duracao_minutos = request.POST.get("duracao_minutos")
        imagem = request.FILES.get("imagem")

        Servico.objects.create(
            nome_servico=nome_servico,
            preco=preco,
            duracao_minutos=duracao_minutos,
            imagem=imagem
        )

        messages.success(
            request,
            "Serviço adicionado com sucesso!"
        )

        return redirect("servico")

    return render(request, 'barber_grid/servico.html')


def usuario_historico(request):
    cliente = Cliente.objects.get(usuario=request.user)

    agendamentos = Agendamento.objects.filter(cliente=cliente)
    
    context = {
        'agendamentos': agendamentos
    }
    return render(request, 'barber_grid/usuario_historico.html', context)