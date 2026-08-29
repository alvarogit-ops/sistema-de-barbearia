from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_POST
from .forms import ClienteForm
from .models import Agendamento, Cliente
def login(request):
    # Verifico se um usuário existe e se a senha está correta

    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        senha = request.POST.get('senha') or ''

        ## Passar um usario obtendo email

        usuario = User.objects.filter(email=email).first()
        user = None
        if usuario is not None:
            user = authenticate(request, username=usuario.username, password=senha)

        # identação corrigia: user não era acessado
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        # redirecionar o usuário para próxima página e com auth_login
        messages.error(request, 'Credenciais inválidas!')

    return render(request, 'barber_grid/login.html') #apontar um app para um template

def registro(request):
    #Aqui eu crio um usuário, os valores vem de uma requisição POST

    if request.method == 'POST':
        nome_usuario = (request.POST.get('nome_usuario') or '').strip()
        email = (request.POST.get('email') or '').strip()
        senha = request.POST.get('senha') or ''
        telefone = (request.POST.get('telefone') or '').strip()
        confirmar_senha = request.POST.get('confirmar_senha') or ''

        if not all([nome_usuario, email, senha, telefone, confirmar_senha]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'barber_grid/registro.html')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não são iguais!')
            return render(request, 'barber_grid/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado!')
            return render(request, 'barber_grid/registro.html')

        if User.objects.filter(username=nome_usuario).exists():
            messages.error(request, 'Este nome de usuário já está cadastrado!')
            return render(request, 'barber_grid/registro.html')

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=nome_usuario,
                    email=email,
                    password=senha,
                )
                Cliente.objects.create(
                    user=user,
                    nome_cliente=nome_usuario,
                    telefone=telefone,
                )
        except IntegrityError:
            messages.error(
                request,
                'Não foi possível concluir o cadastro. Tente outro nome de usuário ou e-mail.',
            )
            return render(request, 'barber_grid/registro.html')

        messages.success(request, 'Conta criada com sucesso. Faça login para continuar.')
        return redirect('login')

    return render(request, 'barber_grid/registro.html')
    #Geralmente no navegador nós acessamos com a requisição GET

@require_POST
def logoutForm(request):
    logout(request)
    return redirect('login') #não deve ser um html

@login_required
def index(request):
    #aqui somente usuários comuns acessam a página home

    if request.user.is_staff:
        return redirect ('painel_admin')

    cliente = Cliente.objects.filter(user=request.user).first()
    agendamentos = (
        Agendamento.objects.filter(usuario=cliente)
        if cliente
        else Agendamento.objects.none()
    )
    return render(
        request,
        'barber_grid/home.html',
        {'agendamentos': agendamentos},
    )

class PerfilProtegido(LoginRequiredMixin):
    pass


def password_change(request):
     if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
     else:
        pass

@login_required
def painel_admin(request):

    if not request.user.is_staff:
        raise PermissionDenied

    agendamentos = Agendamento.objects.all()

    return render(
        request,
        'barber_grid/agendamentos.html',
        {'agendamentos': agendamentos}
    )


@login_required
def clientes(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(
        request,
        'barber_grid/clientes.html',
        {
            'form': form,
            'clientes': Cliente.objects.all(),
        },
    )

