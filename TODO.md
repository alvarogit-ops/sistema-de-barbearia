# TODO - Cadastro simples (Django)

- [x] Criar template HTML de cadastro: `barber_grid/templates/barber_grid/cadastro.html`
  - [x] Campos: Nome de usuário e Senha
  - [x] POST com CSRF
  - [x] Exibir mensagem `message` se existir

- [x] Criar view `cadastro` em `barber_grid/views.py`
  - [x] Receber POST, ler username/password
  - [x] Salvar via `User.objects.create_user`
  - [x] Renderizar template novamente com `message` de sucesso
  - [x] Adicionar comentários explicando como o Django criptografa/salta/hasha a senha

- [x] Atualizar rotas em `barber_grid/urls.py`
  - [x] Adicionar `path('cadastro/', views.cadastro, name='cadastro')`

- [ ] (Opcional) Atualizar `base.html` para link no menu para Cadastro

- [ ] Testar manualmente: rodar servidor e acessar `/cadastro/`

