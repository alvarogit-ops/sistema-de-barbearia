from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

def loginForm(request):
    # Verifico se um usuário existe e se a senha está correta

    if request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        user = authenticate(request, username = nome_usuario, password=senha)

    if user is not None:
        login(request, user)
        # redirecionar o usuário para próxima página
    else:
        raise ValidationError("Credenciais inválidas")

    return render(request, 'accounts/login.html')

def RegisterForm(request):
    #Aqui eu crio um usuário, os valores vem de uma requisição POST

    if request.method == 'POST':
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        user = User.objects.create_user(username = nome_usuario , password = senha)


    #Geralmente no navegador nós acessamos com a requisição GET

def logoutForm(request):
    logout(request, redirect='Sucess')

@login_required
def index(request):
    login_url = '/login/'
    redirect = ''
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