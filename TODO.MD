## Início

1. Iniciar app
2. adicionar barber_grid.app.BarberGridConfig em settings.py
3. Criar urls.py dentro do app
4. Importar HttpResponse do django.http
5. retornar httpresponse com o nome do app
6. Criar url patterns dentro das 2 urls, no admin vai ter caminho para barber_grid urls

## Models

Status: 

* Cliente está como None ao invés de anônimo


1. Criar model de agendamento
2. Impedir que clientes marquem no mesmo horário
3. Se cliente estiver vazio, ele será anônimo
4. Em seguida, relacionar com cliente, barbeiro e serviço
5. Rodar e aplicar as migrações
6. Testar criação de horários com conflito no terminal

## Criação de dados

Status:

* Cliente não existe e não possui telefone
* Agendamento não exibe serviço e cliente

1. Rodar python manage.py shell
2. Importar models e classes
3. Criar agendamento e cliente

## Exibir registros

1. Definir a view e o caminho para barber_grid/agendamento.html
2. Criar pasta de templates
3. Mostrar todas instâncias em views.py importando da classe Agendamento e o contexto
4. Mostrar vários agendamentos com Django Template
5. No shell, usar agendamento.servico.add(servico1) pq é um Many to Many Field
6. Para exibição dos registros, usar expressão geradora para pegar todos serviços relacionados, para cada serviço pegar o nome do serviço.


## Painel Admin

Importar a classe Agendamento em admin.py e colocar register admin para Agendamento
python manage.py createsuperuser
Adicionar agendamento

## Static assets

criar pasta static
importar os
configurar staticfile_dirs
configurar media_url = 'images/'
python
>>> import os
>>> base_dir = os.getcwd()
>>> print(base_dir)

## Autenticação

formulario de senha

## Forms

Arquivo forms.py dentro do app importando forms do django
importar forms dentro de views.py

Criar registro.html, protegido.html, login.html
Em home, request.user.username
usar Csrf token, form as p
Usar javascript para exibir cores e mensagens de erro
Adicionar path authApp.urls e accounts login importando as views de authApp
Adicionar em settings LOGIN_REDIRECT_URL = 'home'


## Corrigir erro de tipo user no Login:

Importar login como auth login em views.py.

Usar email ao invés de nome_usuario
No html, o input recebe email, ao invés de nome_usuario
def registro não está salvando email e telefone, precisa ter validação se a senha e confirmar senha não forem iguais
Adicionar name = "index" em urls.py
usar is_staff para identificar quem pode entrar no painel administrativo.
Validar se email existe no registro pra impedir 2 emails cadastrados

## Erros corrigidos e mudanças

Caminho não apontava para static em arquivos html.
A view de login deve receber somente request e obter o usuário depois da autenticação.
Removida a opção de agendar pelo WhatsApp.
Home passa a ser apenas para usuários autenticados


## Funcionalidade de login

usar a rota de logout e um formulário POST.

## Bugbot

Severity	Location (file:line)	Finding
high
barber_grid/views.py:23
Login lança ValidationError sem tratamento; credenciais inválidas viram HTTP 500 em vez de mensagem no formulário.
high
barber_grid/views.py:48
Registro lança ValidationError sem captura; senhas diferentes ou e-mail já cadastrado viram HTTP 500.
medium
barber_grid/views.py:54
Após create_user bem-sucedido, a view só re-renderiza o cadastro, sem redirecionar nem autenticar.
medium
barber_grid/views.py:45
O campo telefone é lido do POST e não é persistido em nenhum model.
medium
barber_grid/views.py:69
A view index renderiza home.html sem agendamentos no contexto; usuários não staff não veem agendamentos.
medium
barber_grid/views.py:54
Registro valida só e-mail duplicado; username único pode gerar IntegrityError e 500.
medium
barber_grid/views.py:59
logoutForm aceita GET; um recurso malicioso pode encerrar a sessão sem POST/CSRF.