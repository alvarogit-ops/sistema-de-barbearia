from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Agendamento


def index(request):
    return render(request, 'barber_grid/index.html')


def agendamento(request):

    agendamento = Agendamento.objects.order_by('data_agendada')

    context = {'agendamentos': agendamento}
    return render(request, 'barber_grid/agendamento.html', context)


def cadastro(request):
    """Formulário simples de cadastro usando User.objects.create_user."""

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Django não salva a senha em texto puro.
        # create_user() chama internamente User.set_password(password), que:
        # - gera um salt aleatório
        # - aplica um hash criptográfico (PBKDF2 por padrão no Django)
        #   (o algoritmo/hashes exatos dependem da configuração de PASSWORD_HASHERS)

        # - armazena apenas o resultado do hash no campo password do usuário
        # Dessa forma, mesmo que a tabela do banco seja exposta, a senha original não é revelada.
        User.objects.create_user(username=username, password=password)

        return render(request, 'barber_grid/cadastro.html', {'message': 'Usuário cadastrado com sucesso!'})

    return render(request, 'barber_grid/cadastro.html')

#quem é o cliente_id? como vou pegar ele?

