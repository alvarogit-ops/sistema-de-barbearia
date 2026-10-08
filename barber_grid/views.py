
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
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def inicio(request):
    proxima_reserva = None

    if request.user.is_authenticated and not request.user.is_staff:
        cliente = Cliente.objects.get(usuario=request.user)

        agendamentos = Agendamento.objects.filter(
            cliente=cliente
        ).order_by("data", "horario")

        agora = timezone.localtime()

        for agendamento in agendamentos:
            data_horario = datetime.datetime.combine(
                agendamento.data,
                agendamento.horario
            )

            data_horario = timezone.make_aware(data_horario)

            if data_horario >= agora:
                proxima_reserva = agendamento
                break

    return render(
        request,
        "barber_grid/inicio.html",
        {"proxima_reserva": proxima_reserva}
    )

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
                return redirect('inicio')
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
    data = request.GET.get("data")
    agora = timezone.now()
    data_atual = agora.date().strftime("%Y-%m-%d")

   

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
        "data": data, "data_atual": data_atual,}
    )
def horarios_disponiveis(request):
    horarios_disponiveis = []
    data = request.GET.get("data")

    inicio_almoco = datetime.time(12, 0)
    fim_almoco = datetime.time(13, 0)

    funcionamento = HorariodeFuncionamento.objects.get(id=1)

    if data:
        data_convertida = datetime.datetime.strptime(data, "%Y-%m-%d")
        dia_escolhido = data_convertida.weekday()

        if funcionamento.dia_inicio <= dia_escolhido <= funcionamento.dia_fim:

            horario_atual = funcionamento.horario_inicio

            horario_fim = datetime.datetime.combine(
                data_convertida,
                funcionamento.horario_fim
            )

            while True:
                horario_atual_convertido = datetime.datetime.combine(
                    data_convertida,
                    horario_atual
                )

                if horario_atual_convertido >= horario_fim:
                    break

                if inicio_almoco <= horario_atual < fim_almoco:
                    horario_atual_convertido += timedelta(minutes=30)
                    horario_atual = horario_atual_convertido.time()
                    continue

                horario_formatado = horario_atual.strftime("%H:%M")

                horario_ocupado = Agendamento.objects.filter(
                    data=data_convertida.date(),
                    horario=horario_atual,
                ).exclude(
                    status="cancelado"
                ).exists()

                if not horario_ocupado:
                    horarios_disponiveis.append(horario_formatado)

                horario_atual_convertido += timedelta(minutes=30)
                horario_atual = horario_atual_convertido.time()

    return JsonResponse({
        "data": data,
        "horarios_disponiveis": horarios_disponiveis
    })

@login_required
def confirmar_agendamento(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    data = request.GET.get("data")
    horario = request.GET.get("horario")

    if request.method == "POST":
        data = request.POST.get("data")
        horario = request.POST.get("horario")

        cliente = Cliente.objects.get(usuario=request.user)

        horario_ocupado = Agendamento.objects.filter(
            data=data,
            horario=horario,
        ).exclude(
            status="cancelado"
        ).exists()

        if horario_ocupado:
            messages.error(
                request,
                "Este horário já está agendado."
            )
            return redirect(
                "agendamento",
                servico_id=servico_id
            )

        agendamento = Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            data=data,
            horario=horario,
        )

        return redirect(
            "enviado",
            agendamento_id=agendamento.id
        )

    return render(
        request,
        "barber_grid/confirmar-agendamento.html",
        {
            "servico": servico,
            "data": data,
            "horario": horario,
            "servico_id": servico_id,
        }
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

@login_required
def usuario_historico(request):
    cliente = Cliente.objects.get(usuario=request.user)

    agendamentos = Agendamento.objects.filter(
        cliente=cliente
    ).order_by("data", "horario")

    agora = timezone.localtime()

    proximos = []
    historico = []

    for agendamento in agendamentos:
        data_horario = datetime.datetime.combine(
            agendamento.data,
            agendamento.horario
        )

        data_horario = timezone.make_aware(data_horario)

        if data_horario >= agora:
            proximos.append(agendamento)
        else:
            historico.append(agendamento)

    context = {
        "proximos": proximos,
        "historico": historico,
    }

    return render(
        request,
        "barber_grid/usuario_historico.html",
        context
    )

def enviado(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)

    return render(
        request,
        'barber_grid/enviado.html',
        {'agendamento': agendamento}
    )

def detalhe_agendamento(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)

    return render(
        request,
        "barber_grid/detalhe-agendamento.html",
        {"agendamento": agendamento}
    )

def cancelar_agendamento(request, agendamento_id):
    if request.method == "POST":
        agendamento = get_object_or_404(
            Agendamento,
            id=agendamento_id,
            cliente__usuario=request.user
        )

        agendamento.status = "cancelado"
        agendamento.save()

        return JsonResponse({
            "sucesso": True,
            "status": agendamento.get_status_display()
        })

    return JsonResponse({
        "sucesso": False
    }, status=405)