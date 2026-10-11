import datetime
from decimal import Decimal
from functools import wraps

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Agendamento,
    BloqueioHorario,
    Cliente,
    DIAS_FERIADO,
    HorariodeFuncionamento,
    Servico,
)

# ---------------------------------------------------------------------------
# Constantes e helpers
# ---------------------------------------------------------------------------

BARBEIRO_USERNAME = "barbeirofelipe"
INTERVALO_SLOT_MINUTOS = 30
INICIO_ALMOCO = datetime.time(12, 0)
FIM_ALMOCO = datetime.time(13, 0)

# Fonte única de feriados (backend), definida em models.py.
FERIADOS = set(DIAS_FERIADO)


def _minutos(horario):
    return horario.hour * 60 + horario.minute


def _sobrepoe(ini_a, fim_a, ini_b, fim_b):
    return ini_a < fim_b and ini_b < fim_a


def eh_feriado(data):
    return (data.month, data.day) in FERIADOS


def obter_barbeiro():
    """Barbeiro padrão; se não existir, usa o primeiro staff ativo."""
    barbeiro = User.objects.filter(
        username=BARBEIRO_USERNAME, is_staff=True
    ).first()

    if barbeiro is None:
        barbeiro = User.objects.filter(
            is_staff=True, is_active=True
        ).order_by("id").first()

    return barbeiro


def barbeiro_required(view):
    """Exige login e permissão de staff (barbeiro/administrador)."""

    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request, "Acesso restrito à equipe da barbearia."
            )
            return redirect("inicio")
        return view(request, *args, **kwargs)

    return wrapper


def _aware(data, horario):
    return timezone.make_aware(
        datetime.datetime.combine(data, horario),
        timezone.get_current_timezone(),
    )


# ---------------------------------------------------------------------------
# Regras de disponibilidade / agendamento
# ---------------------------------------------------------------------------

def _contexto_dia(data):
    """Busca uma única vez tudo o que é necessário para avaliar o dia."""
    funcionamento = HorariodeFuncionamento.objects.first()

    ocupados = [
        (
            _minutos(ag.horario),
            _minutos(ag.horario) + ag.servico.duracao_minutos,
        )
        for ag in Agendamento.objects.filter(data=data)
        .exclude(status="cancelado")
        .select_related("servico")
    ]

    bloqueios = [
        (_minutos(b.horario_inicio), _minutos(b.horario_fim))
        for b in BloqueioHorario.objects.filter(
            data_inicio__lte=data, data_fim__gte=data
        )
    ]

    return {
        "funcionamento": funcionamento,
        "ocupados": ocupados,
        "bloqueios": bloqueios,
    }


def _motivo_indisponivel(ctx, data, horario, duracao, agora):
    """Retorna a mensagem de erro se o horário não puder ser usado."""
    funcionamento = ctx["funcionamento"]

    if funcionamento is None:
        return "Os horários de funcionamento ainda não foram configurados."

    if eh_feriado(data):
        return "Não é possível agendar em um feriado nacional."

    if not (
        funcionamento.dia_inicio <= data.weekday() <= funcionamento.dia_fim
    ):
        return "A barbearia não atende neste dia da semana."

    inicio = _minutos(horario)
    fim = inicio + duracao
    abertura = _minutos(funcionamento.horario_inicio)
    fechamento = _minutos(funcionamento.horario_fim)

    if inicio < abertura or fim > fechamento:
        return "Horário fora do funcionamento da barbearia."

    if (inicio - abertura) % INTERVALO_SLOT_MINUTOS != 0:
        return "Horário inválido."

    if _aware(data, horario) <= timezone.localtime(agora):
        return "Não é possível agendar para um horário que já passou."

    if _sobrepoe(inicio, fim, _minutos(INICIO_ALMOCO), _minutos(FIM_ALMOCO)):
        return "Este horário conflita com o intervalo de almoço."

    if any(_sobrepoe(inicio, fim, ini, f) for ini, f in ctx["bloqueios"]):
        return "Este horário está bloqueado."

    if any(_sobrepoe(inicio, fim, ini, f) for ini, f in ctx["ocupados"]):
        return "Este horário já está agendado."

    return None


def listar_horarios_livres(data, duracao):
    ctx = _contexto_dia(data)
    funcionamento = ctx["funcionamento"]

    if funcionamento is None:
        return []

    agora = timezone.now()
    livres = []
    atual = _minutos(funcionamento.horario_inicio)
    limite = _minutos(funcionamento.horario_fim)

    while atual + duracao <= limite:
        horario = datetime.time(atual // 60, atual % 60)

        if _motivo_indisponivel(ctx, data, horario, duracao, agora) is None:
            livres.append(horario.strftime("%H:%M"))

        atual += INTERVALO_SLOT_MINUTOS

    return livres


def validar_e_criar_agendamento(
    cliente, servico, barbeiro, data_texto, horario_texto, observacoes=""
):
    """Valida tudo e cria o agendamento. Retorna (agendamento, erro)."""
    try:
        data = datetime.datetime.strptime(data_texto, "%Y-%m-%d").date()
        horario = datetime.datetime.strptime(horario_texto, "%H:%M").time()
    except (ValueError, TypeError):
        return None, "Data ou horário inválido."

    if not servico.ativo:
        return None, "Este serviço não está disponível."

    ctx = _contexto_dia(data)
    erro = _motivo_indisponivel(
        ctx, data, horario, servico.duracao_minutos, timezone.now()
    )

    if erro:
        return None, erro

    try:
        with transaction.atomic():
            agendamento = Agendamento.objects.create(
                cliente=cliente,
                servico=servico,
                barbeiro=barbeiro,
                data=data,
                horario=horario,
                observacoes=(observacoes or "").strip()[:500],
            )
    except IntegrityError:
        return None, (
            "Este horário acabou de ser reservado por outra pessoa. "
            "Escolha outro horário."
        )

    return agendamento, None


# ---------------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------------

@login_required
def inicio(request):
    proxima_reserva = None

    if not request.user.is_staff:
        cliente = Cliente.objects.filter(usuario=request.user).first()

        if cliente is not None:
            agora = timezone.localtime()

            agendamentos = (
                Agendamento.objects.filter(
                    cliente=cliente, data__gte=agora.date()
                )
                .exclude(status="cancelado")
                .select_related("servico")
                .order_by("data", "horario")
            )

            for agendamento in agendamentos:
                if _aware(agendamento.data, agendamento.horario) > agora:
                    proxima_reserva = agendamento
                    break

    return render(
        request,
        "barber_grid/inicio.html",
        {"proxima_reserva": proxima_reserva},
    )


@login_required
def pagina_servicos(request):
    servicos = Servico.objects.filter(ativo=True)
    return render(
        request, "barber_grid/pagina_servicos.html", {"servicos": servicos}
    )


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("senha")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_staff:
                return redirect("painel_admin")
            return redirect("pagina_servicos")

        messages.error(request, "Usuário / senha inválidos")

    return render(request, "barber_grid/login.html")


def registro(request):
    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        telefone = (request.POST.get("telefone") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("senha") or ""

        if not nome or not telefone or not email or not password:
            messages.error(request, "Preencha todos os campos.")
            return render(request, "barber_grid/registro.html")

        if len(telefone) > 15:
            messages.error(request, "Telefone muito longo.")
            return render(request, "barber_grid/registro.html")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Este nome de usuário já está cadastrado.")
            return render(request, "barber_grid/registro.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return render(request, "barber_grid/registro.html")

        try:
            validate_password(password)
        except ValidationError as erro:
            for mensagem in erro.messages:
                messages.error(request, mensagem)
            return render(request, "barber_grid/registro.html")

        with transaction.atomic():
            usuario = User.objects.create_user(
                username=email,
                email=email,
                first_name=nome,
                password=password,
            )
            Cliente.objects.create(usuario=usuario, telefone=telefone)

        messages.success(request, "Conta criada com sucesso!")
        return redirect("login")

    return render(request, "barber_grid/registro.html")


@login_required
def agendamento(request, servico_id):
    """Tela de escolha de data/horário (o POST real é em confirmar_agendamento)."""
    servico = get_object_or_404(Servico, id=servico_id, ativo=True)

    return render(
        request,
        "barber_grid/agendamento.html",
        {
            "servico": servico,
            "data": request.GET.get("data", ""),
            "data_atual": timezone.localdate().strftime("%Y-%m-%d"),
        },
    )


def horarios_disponiveis(request):
    data_texto = request.GET.get("data")

    if not data_texto:
        return JsonResponse(
            {"data": None, "feriado": False, "horarios_disponiveis": []}
        )

    try:
        data = datetime.datetime.strptime(data_texto, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse(
            {
                "data": data_texto,
                "feriado": False,
                "horarios_disponiveis": [],
                "erro": "Data inválida.",
            },
            status=400,
        )

    # Duração do serviço escolhido (opcional): ?servico=<id>
    duracao = INTERVALO_SLOT_MINUTOS
    servico_id = request.GET.get("servico", "")

    if servico_id.isdigit():
        servico = Servico.objects.filter(pk=servico_id, ativo=True).first()
        if servico is not None:
            duracao = servico.duracao_minutos

    feriado = eh_feriado(data)

    return JsonResponse(
        {
            "data": data_texto,
            "feriado": feriado,
            "horarios_disponiveis": (
                [] if feriado else listar_horarios_livres(data, duracao)
            ),
        }
    )


@login_required
def confirmar_agendamento(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id, ativo=True)

    if request.method == "POST":
        if request.user.is_staff:
            messages.error(
                request,
                "Administradores não podem realizar agendamentos por esta página.",
            )
            return redirect("inicio")

        cliente = Cliente.objects.filter(usuario=request.user).first()

        if cliente is None:
            messages.error(
                request, "Seu usuário não possui um cadastro de cliente."
            )
            return redirect("inicio")

        barbeiro = obter_barbeiro()

        if barbeiro is None:
            messages.error(request, "Nenhum barbeiro disponível no momento.")
            return redirect("agendamento", servico_id=servico_id)

        novo, erro = validar_e_criar_agendamento(
            cliente,
            servico,
            barbeiro,
            request.POST.get("data"),
            request.POST.get("horario"),
            request.POST.get("observacoes", ""),
        )

        if erro:
            messages.error(request, erro)
            return redirect("agendamento", servico_id=servico_id)

        return redirect("enviado", agendamento_id=novo.id)

    data = request.GET.get("data", "")
    horario = request.GET.get("horario", "")

    try:
        data_obj = datetime.datetime.strptime(data, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Data ou horário inválido.")
        return redirect("agendamento", servico_id=servico_id)

    return render(
        request,
        "barber_grid/confirmar-agendamento.html",
        {
            "servico": servico,
            "data": data,          # ISO, para o campo hidden
            "data_obj": data_obj,  # use {{ data_obj|date:"d/m/Y" }} no template
            "horario": horario,
            "servico_id": servico_id,
        },
    )


@login_required
def usuario_historico(request):
    cliente = Cliente.objects.filter(usuario=request.user).first()

    if cliente is None:
        messages.error(
            request, "Seu usuário não possui um cadastro de cliente."
        )
        return redirect("inicio")

    agendamentos = (
        Agendamento.objects.filter(cliente=cliente)
        .select_related("servico")
        .order_by("data", "horario")
    )

    agora = timezone.localtime()
    proximos = []
    historico = []

    for item in agendamentos:
        if _aware(item.data, item.horario) >= agora:
            proximos.append(item)
        else:
            historico.append(item)

    return render(
        request,
        "barber_grid/usuario_historico.html",
        {"proximos": proximos, "historico": historico},
    )


@login_required
def enviado(request, agendamento_id):
    agendamento_obj = get_object_or_404(
        Agendamento.objects.select_related("servico"),
        id=agendamento_id,
        cliente__usuario=request.user,
    )

    return render(
        request,
        "barber_grid/enviado.html",
        {"agendamento": agendamento_obj},
    )


@login_required
def detalhe_agendamento(request, agendamento_id):
    filtros = {"id": agendamento_id}

    if not request.user.is_staff:
        filtros["cliente__usuario"] = request.user

    agendamento_obj = get_object_or_404(
        Agendamento.objects.select_related("servico"), **filtros
    )

    return render(
        request,
        "barber_grid/detalhe-agendamento.html",
        {"agendamento": agendamento_obj},
    )


@login_required
def cancelar_agendamento(request, agendamento_id):
    if request.method != "POST":
        return JsonResponse({"sucesso": False}, status=405)

    agendamento_obj = get_object_or_404(
        Agendamento,
        id=agendamento_id,
        cliente__usuario=request.user,
    )

    agendamento_obj.status = "cancelado"
    agendamento_obj.save(update_fields=["status"])

    return JsonResponse(
        {"sucesso": True, "status": agendamento_obj.get_status_display()}
    )


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("login")

    return redirect("inicio")


@login_required
def editar_perfil(request):
    if request.user.is_staff:
        return redirect("editar_perfil_admin")

    cliente = Cliente.objects.filter(usuario=request.user).first()

    if cliente is None:
        messages.error(
            request, "Não foi encontrado um perfil de cliente para esta conta."
        )
        return redirect("pagina_servicos")

    contexto = {"cliente": cliente}

    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        email = (request.POST.get("email") or "").strip()
        telefone = (request.POST.get("telefone") or "").strip()
        foto = request.FILES.get("foto")

        if not nome or not email or not telefone:
            messages.error(request, "Preencha todos os campos.")
            return render(request, "barber_grid/editar_perfil.html", contexto)

        if len(telefone) > 15:
            messages.error(request, "Telefone muito longo.")
            return render(request, "barber_grid/editar_perfil.html", contexto)

        em_uso = (
            User.objects.filter(email=email) | User.objects.filter(username=email)
        ).exclude(pk=request.user.pk)

        if em_uso.exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return render(request, "barber_grid/editar_perfil.html", contexto)

        with transaction.atomic():
            request.user.first_name = nome
            request.user.email = email
            request.user.username = email
            request.user.save()

            cliente.telefone = telefone

            if foto:
                cliente.foto_perfil = foto

            cliente.save()

        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect("usuario_historico")

    return render(request, "barber_grid/editar_perfil.html", contexto)


@login_required
def alterar_senha(request):
    if request.method == "POST":
        formulario = PasswordChangeForm(user=request.user, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.save()
            update_session_auth_hash(request, usuario)

            messages.success(request, "Senha alterada com sucesso.")

            if usuario.is_staff:
                return redirect("editar_perfil_admin")

            return redirect("editar_perfil")
    else:
        formulario = PasswordChangeForm(user=request.user)

    # alterar_senha.html usa "form"; mantido "formulario" por compatibilidade.
    return render(
        request,
        "barber_grid/alterar_senha.html",
        {"formulario": formulario, "form": formulario},
    )


@require_POST
def solicitar_redefinicao_senha_ajax(request):
    form = PasswordResetForm(data=request.POST)

    if form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            email_template_name="barber_grid/email_redefinir_senha.html",
            subject_template_name="barber_grid/assunto_redefinir_senha.txt",
        )

    return JsonResponse(
        {
            "mensagem": (
                "Se o e-mail estiver cadastrado, você receberá "
                "um link para criar uma nova senha."
            )
        }
    )


# ---------------------------------------------------------------------------
# Administração / barbeiro
# ---------------------------------------------------------------------------

@barbeiro_required
def painel_admin(request):
    data_selecionada = request.GET.get("data", "")
    status_selecionado = request.GET.get("status", "")

    try:
        data_agenda = (
            datetime.datetime.strptime(data_selecionada, "%Y-%m-%d").date()
            if data_selecionada
            else timezone.localdate()
        )
    except ValueError:
        data_agenda = timezone.localdate()

    agendamentos = (
        Agendamento.objects.filter(barbeiro=request.user, data=data_agenda)
        .select_related("cliente__usuario", "servico", "barbeiro")
        .order_by("horario")
    )

    if status_selecionado:
        agendamentos = agendamentos.filter(status=status_selecionado)

    return render(
        request,
        "barber_grid/painel_admin.html",
        {
            "agendamentos": agendamentos,
            "data_agenda": data_agenda.strftime("%Y-%m-%d"),
            "status_selecionado": status_selecionado,
        },
    )


@barbeiro_required
def historico_agendamentos(request):
    # Página antiga, fora do padrão. Recomendado remover view, rota e template.
    agendamentos = Agendamento.objects.select_related(
        "cliente__usuario", "servico"
    ).order_by("-data", "-horario")

    return render(
        request,
        "barber_grid/historico_agendamentos.html",
        {"agendamentos": agendamentos},
    )


@barbeiro_required
def admin_confirmar(request):
    if request.method == "POST":
        agendamento_id = request.POST.get("agendamento_id")
        acao = request.POST.get("acao")

        if not (agendamento_id or "").isdigit():
            messages.error(request, "Agendamento inválido.")
            return redirect("admin_confirmar")

        agendamento_obj = get_object_or_404(
            Agendamento, id=agendamento_id, barbeiro=request.user
        )

        if agendamento_obj.status != "solicitado":
            messages.error(
                request,
                "Este agendamento não está mais aguardando confirmação.",
            )
            return redirect("admin_confirmar")

        if acao == "confirmar":
            agendamento_obj.status = "confirmado"
            agendamento_obj.save(update_fields=["status"])
            messages.success(request, "Agendamento confirmado com sucesso!")

        elif acao == "cancelar":
            agendamento_obj.status = "cancelado"
            agendamento_obj.save(update_fields=["status"])
            messages.success(request, "Agendamento cancelado com sucesso!")

        else:
            messages.error(request, "Ação inválida.")

        return redirect("admin_confirmar")

    agendamentos = (
        Agendamento.objects.filter(barbeiro=request.user, status="solicitado")
        .select_related("cliente__usuario", "servico", "barbeiro")
        .order_by("data", "horario")
    )

    return render(
        request,
        "barber_grid/admin_confirmar.html",
        {"agendamentos": agendamentos},
    )


@user_passes_test(lambda user: user.is_staff)
def dados_negocio(request):
    return render(request, "barber_grid/dados_negocio.html")


@login_required
def editar_perfil_admin(request):
    usuario = request.user

    if not usuario.is_staff:
        messages.error(request, "Acesso permitido apenas ao administrador.")
        return redirect("inicio")

    cliente = Cliente.objects.filter(usuario=usuario).first()

    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        email = (request.POST.get("email") or "").strip()
        foto = request.FILES.get("foto")

        if not nome or not email:
            messages.error(request, "Preencha todos os campos.")

        elif User.objects.filter(email=email).exclude(pk=usuario.pk).exists():
            messages.error(request, "Este e-mail já está cadastrado.")

        else:
            usuario.first_name = nome
            usuario.email = email
            usuario.save()

            if foto:
                cliente, _ = Cliente.objects.get_or_create(
                    usuario=usuario, defaults={"telefone": ""}
                )
                cliente.foto_perfil = foto
                cliente.save(update_fields=["foto_perfil"])

            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("editar_perfil_admin")

    return render(
        request,
        "barber_grid/editar_perfil_admin.html",
        {"usuario": usuario, "cliente": cliente},
    )


@staff_member_required
def alterar_senha_admin(request):
    if request.method == "POST":
        formulario = PasswordChangeForm(user=request.user, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.save()
            update_session_auth_hash(request, usuario)

            messages.success(request, "Senha alterada com sucesso.")
            return redirect("alterar_senha_admin")
    else:
        formulario = PasswordChangeForm(user=request.user)

    return render(
        request,
        "barber_grid/alterar_senha_admin.html",
        {"formulario": formulario},
    )


@staff_member_required
def lista_servicos(request):
    servicos = Servico.objects.all()
    ativo = request.GET.get("ativo")

    if ativo == "true":
        servicos = servicos.filter(ativo=True)
    elif ativo == "false":
        servicos = servicos.filter(ativo=False)

    return render(
        request, "barber_grid/servicos.html", {"servicos": servicos}
    )


@staff_member_required
def servico(request):
    if request.method == "POST":
        nome_servico = (request.POST.get("nome_servico") or "").strip()
        preco_texto = (request.POST.get("preco") or "").strip()
        duracao_texto = (request.POST.get("duracao_minutos") or "").strip()
        imagem = request.FILES.get("imagem")

        # O formulário novo_servico.html não tem checkbox "ativo": se o campo
        # não vier, o serviço nasce ativo (antes nascia sempre inativo).
        ativo = request.POST.get("ativo", "on") == "on"

        if not nome_servico or not preco_texto or not duracao_texto:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return render(request, "barber_grid/novo_servico.html")

        try:
            preco = Decimal(preco_texto.replace(",", "."))
            duracao_minutos = int(duracao_texto)

            if (
                not preco.is_finite()
                or preco < 0
                or preco >= Decimal("100000000")
                or duracao_minutos <= 0
            ):
                raise ValueError

            preco = preco.quantize(Decimal("0.01"))

        except (ValueError, TypeError, ArithmeticError):
            messages.error(request, "Informe um preço e uma duração válidos.")
            return render(request, "barber_grid/novo_servico.html")

        Servico.objects.create(
            nome_servico=nome_servico,
            preco=preco,
            duracao_minutos=duracao_minutos,
            imagem=imagem,
            ativo=ativo,
        )

        messages.success(request, "Serviço adicionado com sucesso!")
        return redirect("servico")

    return render(request, "barber_grid/novo_servico.html")