
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
import datetime
from datetime import timedelta
from .models import Servico, Cliente, Agendamento, HorariodeFuncionamento, BloqueioHorario
from django.http import JsonResponse


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

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Este nome de usuário já está cadastrado.')
            return render(request, 'barber_grid/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'barber_grid/registro.html')

        usuario = User.objects.create_user(
            username=email,
            password=password
        )

        Cliente.objects.create(
            usuario=usuario,
            telefone=telefone
        )

        messages.success(request, 'Conta criada com sucesso!')

        return redirect('login')

    return render(request, 'barber_grid/registro.html')


def agendamento(request, servico_id):
    servico = Servico.objects.get(id=servico_id)
    horarios_disponiveis = []
    data = request.GET.get("data")

    if data:

        data_convertida = datetime.datetime.strptime(data, "%Y-%m-%d")
        funcionamento = HorariodeFuncionamento.objects.get(id=1)
        dia_escolhido = data_convertida.weekday()

        if dia_escolhido >= funcionamento.dia_inicio and dia_escolhido <= funcionamento.dia_fim:
                    horario_atual = funcionamento.horario_inicio
                    horario_atual_convertido = datetime.datetime.combine(data_convertida, horario_atual)
                    funcionamento.horario_fim = datetime.datetime.combine(data_convertida, funcionamento.horario_fim)
                    while horario_atual_convertido < funcionamento.horario_fim:
                        horarios_disponiveis.append(horario_atual_convertido)
                        horario_atual_convertido = horario_atual_convertido + timedelta(minutes=30)
                        print(horarios_disponiveis)

    if request.method == "POST":
        data = request.POST.get("data")
        horario = request.POST.get("horario")

        cliente = Cliente.objects.get(usuario=request.user)

        if Agendamento.objects.filter(data=data, horario=horario).exists():

            messages.error(
                request,
                "Este horário já está agendado."
            )

            return redirect(
                "agendamento",
                servico_id=servico_id
            )


        data_horario = datetime.datetime.strptime(data + " " + horario, "%Y-%m-%d %H:%M")
        data_horario = timezone.make_aware(data_horario)
        agora = timezone.now()
        if data_horario < agora:
            messages.error(
                request,
                "Agende um horário posterior."
            )

            return redirect("agendamento", servico_id=servico_id)
        
        


        


        Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            data=data,
            horario=horario,
        )

        messages.success(
            request,
            "Agendamento feito com sucesso!"
        )

        return redirect("usuario_historico")

    print("AGENDAMENTO:", request.method, request.GET, request.POST)

    return render(
        request,
        "barber_grid/agendamento.html",
        {"servico": servico,
        "horarios_disponiveis": horarios_disponiveis,
        "data": data}
    )
def horarios_disponiveis(request):
    
    data = request.GET.get("data")
    print("DATA RECEBIDA:", data)
    funcionamento = HorariodeFuncionamento.objects.get(id=1)
    print("ABRE:", funcionamento.horario_inicio)
    print("FECHA:", funcionamento.horario_fim)  
    return JsonResponse({"data": data})


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