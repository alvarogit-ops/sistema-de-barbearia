from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from .models import Agendamento
def login(request):
    # Verifico se um usuário existe e se a senha está correta

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        ## Passar um usario obtendo email

        try:
            usuario = User.objects.get(email=email)

        except User.DoesNotExist:
            raise ValidationError('Credenciais inválidas!')

        user = authenticate(request, username=usuario.username, password=senha)

        # identação corrigia: user não era acessado
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        # redirecionar o usuário para próxima página e com auth_login
        else:
            raise ValidationError("Credenciais inválidas")

    return render(request, 'barber_grid/login.html') #apontar um app para um template

def registro(request):
    #Aqui eu crio um usuário, os valores vem de uma requisição POST

    if request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        email = request.POST['email']
        senha = request.POST['senha']
        telefone = request.POST['telefone']
        confirmar_senha = request.POST['confirmar_senha']

        if senha != confirmar_senha:
            raise ValidationError("As senhas não são iguais!")

        if User.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já está cadastrado!')

        user = User.objects.create_user(username = nome_usuario , email=email, password = senha)

    return render(request, 'barber_grid/registro.html')
    #Geralmente no navegador nós acessamos com a requisição GET

def logoutForm(request):
    logout(request, redirect='Sucess')

@login_required
def index(request):
    return render(request, 'barber_grid/home.html')

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

