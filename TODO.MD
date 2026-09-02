<<<<<<< HEAD
# Início

- Iniciar o aplicativo Django.
- Adicionar `barber_grid.app.BarberGridConfig` em `INSTALLED_APPS` no `settings.py`.
- Criar `urls.py` dentro do app `barber_grid`.
- Importar `HttpResponse` de `django.http`.
- Criar uma resposta HTTP simples para testar o funcionamento do app.
- Configurar as URLs do projeto para encaminhar as requisições para `barber_grid.urls`.
- Criar os primeiros `urlpatterns` do projeto e do aplicativo.

# Models

## Status inicial

- Cliente estava como `None` em determinados agendamentos, representando um cliente anônimo.
- Criar o model `Agendamento`.
- Criar a regra para impedir dois agendamentos no mesmo horário.
- Permitir inicialmente que `Cliente` pudesse ficar vazio, representando um agendamento anônimo.
- Relacionar `Agendamento` com `Cliente`, `Barbeiro` e `Servico`.
- Executar e aplicar as migrações do banco de dados.
- Testar a criação de agendamentos com conflito de horário pelo terminal.
- Utilizar relacionamentos `ManyToMany` quando necessário.

# Criação de dados pelo Shell

## Problemas identificados posteriormente

- Cliente não estava sendo criado corretamente.
- Agendamento não exibia serviço e cliente.
- Executar `python manage.py shell`.
- Importar os models e classes necessárias.
- Criar registros de clientes.
- Criar registros de serviços.
- Criar agendamentos manualmente.
- Associar serviços aos agendamentos.
- Testar os relacionamentos entre os models.

# Exibição de registros

- Criar a view responsável pela exibição dos agendamentos.
- Definir a URL para a página de agendamentos.
- Criar a estrutura de templates do projeto.
- Criar `barber_grid/agendamentos.html`.
- Buscar as instâncias de `Agendamento` em `views.py`.
- Passar os agendamentos para o template através do contexto.
- Utilizar Django Templates para percorrer e exibir vários agendamentos.
- Utilizar `agendamento.servico.add(servico1)` para associar serviços ao `ManyToManyField`.
- Utilizar expressões geradoras para obter os serviços relacionados e exibir seus nomes.

# Painel Admin

- Importar `Agendamento` em `admin.py`.
- Registrar `Agendamento` utilizando `admin.site.register()`.
- Criar um superusuário com `python manage.py createsuperuser`.
- Acessar o painel administrativo do Django.
- Criar e visualizar agendamentos pelo Django Admin.

# Static Assets

- Criar a pasta `static`.
- Importar `os`.
- Configurar `STATICFILES_DIRS`.
- Configurar `MEDIA_URL`.
- Utilizar `os.getcwd()` para verificar o diretório atual pelo Python Shell.
- Corrigir caminhos que não apontavam corretamente para os arquivos estáticos nos templates.
- Configurar a utilização de CSS e JavaScript no projeto.

# Autenticação

- Criar formulário de senha.
- Criar página de login.
- Criar página de registro.
- Criar página protegida para usuários autenticados.
- Utilizar autenticação nativa do Django.
- Utilizar `request.user` para identificar o usuário autenticado.
- Utilizar `{% csrf_token %}` nos formulários.
- Utilizar `@login_required` para proteger páginas.
- Configurar `LOGIN_REDIRECT_URL`.
- Criar rota de logout utilizando requisição `POST`.
- Utilizar `is_staff` para diferenciar usuários administrativos de usuários comuns.

# Forms

- Criar `forms.py` dentro do app.
- Importar `forms` do Django.
- Criar formulários utilizando Django Forms.
- Importar os formulários em `views.py`.
- Integrar os formulários aos templates.
- Utilizar `{{ form }}` para renderização dos campos.
- Exibir mensagens e erros de validação nos templates.
- Utilizar JavaScript para auxiliar na exibição de mensagens e alterações visuais.

# Registro e Login

- Corrigir o tratamento do usuário durante o processo de autenticação.
- Importar `login` como `auth_login` em `views.py` para evitar conflito de nomes.
- Alterar o login para utilizar e-mail como credencial.
- Alterar o campo HTML de `nome_usuario` para `email` no formulário de login.
- Corrigir o cadastro para persistir e-mail e telefone.
- Validar se senha e confirmação de senha são iguais.
- Validar se o e-mail já está cadastrado.
- Validar se o nome de usuário já está cadastrado.
- Utilizar `create_user()` para criação dos usuários.
- Criar o relacionamento entre `User` e `Cliente`.
- Adicionar `name="index"` à URL da página inicial.
- Utilizar `is_staff` para direcionar administradores ao painel administrativo.
- Configurar o redirecionamento após o login.

# Funcionalidade de Agendamento

- Criar o formulário de agendamento.
- Permitir seleção de serviço.
- Permitir seleção de data.
- Permitir seleção de horário.
- Associar o agendamento ao cliente autenticado.
- Validar os dados do formulário.
- Impedir conflitos de horário.
- Exibir mensagens de sucesso e erro.
- Exibir os agendamentos do cliente na Home.
- Remover a opção de agendamento pelo WhatsApp.
- Tornar a Home acessível somente para usuários autenticados.

# AJAX

- Criar `script.js`.
- Capturar o formulário de agendamento pelo JavaScript.
- Interceptar o envio tradicional do formulário.
- Utilizar `fetch()` para enviar o formulário via `POST`.
- Enviar os dados utilizando `FormData`.
- Identificar a requisição como AJAX através de `X-Requested-With`.
- Criar respostas `JsonResponse` no Django.
- Retornar o HTML da lista de agendamentos dentro do JSON.
- Atualizar a lista de agendamentos sem recarregar a página.
- Retornar o HTML atualizado do formulário quando houver erros de validação.
- Substituir o formulário antigo pelo formulário atualizado.
- Desabilitar o botão durante o processamento.
- Exibir o estado `"Agendando..."`.
- Tratar erros no JavaScript.
- Corrigir o problema de resposta HTML sendo interpretada como JSON.
- Finalizar a implementação do fluxo AJAX de agendamento.

# Erros corrigidos e mudanças

- Corrigir caminhos de arquivos estáticos nos templates.
- Corrigir o fluxo de autenticação.
- Corrigir o uso de `login` em `views.py`.
- Corrigir persistência de e-mail e telefone no registro.
- Adicionar validações no cadastro.
- Adicionar proteção das páginas autenticadas.
- Adicionar diferenciação entre usuário comum e administrador.
- Remover a opção de agendamento pelo WhatsApp.
- Corrigir a exibição dos agendamentos na Home.
- Corrigir o logout para utilizar `POST`.
- Corrigir o tratamento de conflitos de horário.
- Corrigir o retorno das requisições AJAX.
- Corrigir a interpretação de respostas HTML como JSON.

# Bugbot

## Problemas identificados

### Alta prioridade

- `barber_grid/views.py:23` — Login poderia lançar `ValidationError` sem tratamento, resultando em erro HTTP 500 em vez de mensagem no formulário.
- `barber_grid/views.py:48` — Registro poderia lançar `ValidationError` sem captura, resultando em HTTP 500.

### Média prioridade

- `barber_grid/views.py:54` — Após `create_user()` bem-sucedido, o fluxo de registro precisava de redirecionamento/autenticação adequada.
- `barber_grid/views.py:45` — O telefone era recebido pelo `POST`, mas não estava sendo persistido corretamente.
- `barber_grid/views.py:69` — A Home precisava receber os agendamentos no contexto.
- `barber_grid/views.py:54` — O username também precisava ser validado para evitar `IntegrityError`.
- `barber_grid/views.py:59` — O logout deveria aceitar somente `POST`, evitando encerramento de sessão através de requisição `GET`.

# Docker

## Em andamento

- Criar `Dockerfile`.
- Criar `requirements.txt`.
- Criar `.dockerignore`.
- Configurar o Django para executar dentro de um container.
- Expor a porta `8000`.
- Criar a imagem Docker do Barber Grid.
- Executar o container.
- Resolver o problema de inicialização do Docker Engine no Windows.
=======
## Improve Ui/Ux:

1. Adicionar favicon
2. Rota para logotipo: carregar apenas com static, sem a url
>>>>>>> a3678fd (style: ajusta espaçamento da seção de agendamentos)
