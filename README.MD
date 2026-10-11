<div align="center">

# 💈 Barber Grid

**Sistema web para consulta de serviços e agendamento de horários em uma barbearia.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-750014?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br>

[📋 Sobre](#-sobre-o-projeto) •
[🚀 Funcionalidades](#-funcionalidades) •
[🛠️ Tecnologias](#️-tecnologias-utilizadas) •
[🏗️ Arquitetura](#️-arquitetura-mvt) •
[⚙️ Como executar](#️-como-executar-o-projeto) •
[🗺️ Roadmap](#️-roadmap) •
[📚 Documentação](#-documentação--links)

<br>

</div>

---

## 📋 Sobre o projeto

O **Barber Grid** é uma aplicação web desenvolvida com Django para gestão de agendamentos em barbearias. A plataforma conecta clientes e o barbeiro em uma interface simples e responsiva: o cliente navega pelos serviços, escolhe um dia e um horário livre e acompanha a confirmação; o barbeiro visualiza a agenda do dia e confirma ou cancela as solicitações.

O projeto segue o padrão **MVT (Model-View-Template)** do Django, com validações de data, horário, feriado e conflito feitas no backend e uma restrição no banco de dados que impede dois agendamentos ativos no mesmo horário.

> **Status:** em desenvolvimento. A seção [Roadmap](#️-roadmap) lista o que já funciona e o que ainda está planejado.

---

## 🚀 Funcionalidades

### 👤 Área do cliente

- **Cadastro e login:** registro com nome, telefone, e-mail e senha (validada pelas regras de senha do Django). O e-mail é usado como nome de usuário.
- **Catálogo de serviços:** cards com imagem, preço e duração estimada.
- **Horários disponíveis:** consulta assíncrona (`fetch`) dos horários livres de um dia, em intervalos de 30 minutos, respeitando horário de funcionamento, pausa de almoço (12h–13h), feriados nacionais fixos, horários já passados e horários já ocupados.
- **Agendamento em 3 passos:** escolha do serviço → escolha de data e horário → confirmação, com tela de "agendamento enviado".
- **Minhas reservas:** abas *Próximas* e *Histórico*, com status (Solicitado, Confirmado, Cancelado) e tela de detalhes.
- **Cancelamento:** o cliente cancela o próprio agendamento pela tela de detalhes, sem recarregar a página.
- **Perfil:** edição de nome, e-mail, telefone e foto; alteração de senha.
- **Recuperação de senha:** solicitação por e-mail com link de redefinição (em desenvolvimento, o e-mail é exibido no console do servidor).
- **Tema claro/escuro** automático conforme a preferência do sistema.

### 💈 Área do barbeiro / administrador

- **Agenda do dia:** navegação por dia (anterior/próximo) e filtro por status.
- **Agendamentos a confirmar:** lista de solicitações pendentes com ações de confirmar e cancelar.
- **Serviços:** listagem com filtro de ativos/inativos e cadastro de novos serviços (nome, preço, duração, imagem e status ativo).
- **Perfil e senha** do administrador.
- **Django Admin** (`/admin/`) para cadastrar o horário de funcionamento e os demais dados.

> O painel do barbeiro é restrito ao usuário `barbeirofelipe` (veja [Primeiro acesso](#6-primeiro-acesso-importante)).

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Função / utilização |
|---|---|
| 🐍 **Python 3.10+** | Linguagem principal do backend |
| 🟢 **Django 6.1** | Framework web (rotas, ORM, autenticação, MVT) |
| 🖼️ **Pillow** | Processamento e upload de imagens (serviços e fotos de perfil) |
| 🌐 **HTML5 / CSS3** | Estrutura semântica e estilização customizada |
| 🟣 **Bootstrap 5.3 + Bootstrap Icons** | Componentes visuais responsivos e ícones |
| 🟨 **JavaScript (ES6+)** | Busca de horários, navegação de datas, cancelamento e tema |
| 🗃️ **SQLite** | Banco de dados do ambiente de desenvolvimento |
| 🔧 **Git & GitHub** | Controle de versão |

---

## 🏗️ Arquitetura (MVT)

```text
               ┌────────────────────────────────────────┐
               │              Navegador                 │
               └───────────────────┬────────────────────┘
                                   │  HTTP Request
                                   ▼
                       ┌───────────────────────┐
                       │  URL Router (urls.py) │
                       └───────────┬───────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │   Views (views.py)    │
                       └─────┬───────────┬─────┘
                             │           │
            Consulta / Salva │           │ Renderiza com contexto
                             ▼           ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│     Models (models.py)       │   │   Templates (HTML/CSS/JS)    │
│ (Servico, Agendamento, etc.) │   │ (inicio.html, login.html...) │
└──────────────────────────────┘   └──────────────────────────────┘
```

---

## 🗃️ Modelos principais

- **`Servico`**: `nome_servico`, `preco`, `duracao_minutos`, `imagem` e `ativo`.
- **`Cliente`**: vinculado ao `User` nativo do Django (`OneToOneField`), com `telefone` e `foto_perfil`.
- **`HorariodeFuncionamento`**: dias da semana (`dia_inicio`, `dia_fim`) e faixa de horário (`horario_inicio`, `horario_fim`). O sistema usa o registro de `id=1`.
- **`BloqueioHorario`**: intervalo de datas e horas bloqueadas, com motivo. *Cadastrável no Django Admin, ainda não aplicado ao cálculo de horários (veja o Roadmap).*
- **`Agendamento`**: conecta `Cliente`, `Servico` e `barbeiro` (`User`) a uma `data` e um `horario`, com `status` (`solicitado`, `confirmado`, `cancelado`). Uma `UniqueConstraint` condicional (`unico_agendamento_ativo`) garante que não existam dois agendamentos não cancelados no mesmo dia e horário.

---

## 🔗 Principais rotas

| Rota | Descrição | Acesso |
|---|---|---|
| `/` | Início e próxima reserva | Logado |
| `/login`, `/registro` | Autenticação | Público |
| `/pagina_servicos` | Catálogo de serviços | Logado |
| `/agendamento/<servico_id>/` | Escolha de data e horário | Logado |
| `/horarios-disponiveis/?data=AAAA-MM-DD` | JSON com horários livres | Público |
| `/confirmar-agendamento/<servico_id>` | Confirmação do agendamento | Logado |
| `/usuario_historico` | Minhas reservas | Logado |
| `/detalhe-agendamento/<id>/` | Detalhes e cancelamento | Logado |
| `/editar-perfil/`, `/alterar-senha/` | Perfil do cliente | Logado |
| `/esqueci-senha/` | Recuperação de senha | Público |
| `/painel_admin` | Agenda do dia | Barbeiro |
| `/painel/confirmar/` | Agendamentos a confirmar | Barbeiro |
| `/painel/servicos/`, `/painel/servicos/novo/` | Gestão de serviços | Staff |

---

## 📁 Estrutura do projeto

```text
sistema-de-barbearia/
│
├── config/                  # Configurações globais (settings.py, urls.py, wsgi/asgi)
├── barber_grid/             # App principal
│   ├── migrations/          # Migrações do banco de dados
│   ├── static/
│   │   ├── css/estilo.css   # Estilos customizados
│   │   └── js/script.js     # Scripts de interface
│   ├── templates/
│   │   └── barber_grid/     # Templates (base.html, base_admin.html e páginas)
│   ├── admin.py             # Registro de models no Django Admin
│   ├── apps.py
│   ├── models.py            # Servico, Cliente, HorariodeFuncionamento,
│   │                        # BloqueioHorario, Agendamento
│   ├── tests.py             # Testes automatizados (em reescrita)
│   ├── urls.py              # Rotas do app
│   └── views.py             # Regras de negócio e views
├── media/                   # Uploads (imagens de serviços e fotos de perfil)
├── anotacoes.md             # Anotações de estudo
├── manage.py                # Utilitário de linha de comando do Django
├── requirements.txt         # Dependências do projeto
└── README.md
```

---

## ⚙️ Como executar o projeto

### Pré-requisitos

- **Python 3.10+** instalado
- **Git** instalado

### 1. Clonar o repositório

```bash
git clone https://github.com/alvarogit-ops/sistema-de-barbearia.git
cd sistema-de-barbearia
```

### 2. Criar e ativar o ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

Caso prefira instalar direto: `pip install django pillow`

### 4. Aplicar as migrações

```bash
python manage.py migrate
```

### 5. Criar o usuário do barbeiro

```bash
python manage.py createsuperuser
```

> ⚠️ Use o nome de usuário **`barbeirofelipe`**. Por enquanto, o sistema procura exatamente esse usuário para atribuir os agendamentos e liberar o painel do barbeiro.

### 6. Primeiro acesso (importante)

Antes de testar o agendamento, acesse **http://127.0.0.1:8000/admin/** com o superusuário e cadastre:

1. **Horário de funcionamento** (um único registro): por exemplo, dia início `Segunda-Feira`, dia fim `Sábado`, das `08:00` às `18:00`. Sem esse registro, a tela de horários retorna erro.
2. **Serviços**: nome, preço e duração (ou use a tela `/painel/servicos/novo/` logado como barbeiro).

Depois crie uma conta de cliente em `/registro` para testar o fluxo completo.

### 7. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/**

### Observações sobre a configuração

- O `settings.py` atual está configurado para **desenvolvimento** (`DEBUG = True`, SQLite, e-mails no console, fuso `America/Recife`). A leitura de variáveis de ambiente (`.env`) ainda não foi implementada — veja o Roadmap.
- Os e-mails de recuperação de senha aparecem no **terminal** onde o servidor está rodando.

---

## 🧪 Testes automatizados

```bash
python manage.py test barber_grid
```

> ⚠️ O arquivo `tests.py` ainda está desatualizado em relação aos models e rotas atuais e está sendo reescrito. Até lá, a execução pode falhar.

---

## 🗺️ Roadmap

### ✅ Implementado

- [x] Cadastro, login, logout, alteração e recuperação de senha
- [x] Catálogo de serviços com imagem, preço e duração
- [x] Consulta de horários livres (funcionamento, almoço, feriados, ocupados)
- [x] Agendamento com validação de data/horário passado, feriado e conflito
- [x] Constraint no banco contra agendamentos ativos duplicados
- [x] Minhas reservas (próximas/histórico), detalhes e cancelamento
- [x] Agenda do dia e confirmação/cancelamento pelo barbeiro
- [x] Cadastro e listagem de serviços (com filtro ativo/inativo)
- [x] Perfil com foto para cliente e administrador
- [x] Tema claro/escuro automático

### 🚧 Em andamento / planejado

- [ ] Reescrever a suíte de testes automatizados
- [ ] Aplicar `BloqueioHorario` no cálculo de horários disponíveis
- [ ] Considerar a duração do serviço na disponibilidade dos horários
- [ ] Editar e remover serviços; ocultar serviços inativos para clientes
- [ ] Salvar o campo "Observações" do agendamento
- [ ] Tela "Dados do negócio" funcional
- [ ] Suporte a mais de um barbeiro (hoje o barbeiro é fixo no código)
- [ ] Ler `SECRET_KEY` e `DEBUG` de variáveis de ambiente (`.env`)
- [ ] Proteger as telas de detalhe/histórico para que cada cliente veja apenas os próprios dados
- [ ] Centralizar a lista de feriados no backend
- [ ] Consolidar as validações de agendamento em uma única função

---

## 📚 Documentação & links

- 🎨 **[Protótipo no Figma](https://www.figma.com/design/DEjI9zGjpfAGLJwP4ejRe2/Barber-Scheduling---Prot%C3%B3tipo-de-Alta-Fidelidade?node-id=0-1&t=wsz3jwY1O719cKFE-1)**
- 📘 [Documentação do Django](https://docs.djangoproject.com/)
- 📘 [Documentação do Bootstrap 5.3](https://getbootstrap.com/docs/5.3/)

---

## 👥 Equipe & desenvolvimento

| Nome | Função | GitHub |
|---|---|---|
| **Álvaro Yuri** | Project Owner, Scrum Master e Desenvolvedor Full-Stack | [@alvarogit-ops](https://github.com/alvarogit-ops) |

---

## 📌 Informações acadêmicas

| Campo | Detalhes |
|---|---|
| **Instituição** | Instituto Federal do Rio Grande do Norte (IFRN) — Campus São Paulo do Potengi |
| **Curso** | Tecnologia em Sistemas para Internet |
| **Disciplina** | Projeto de Desenvolvimento de Sistemas para Internet |
| **Professora** | Fernanda Lígia |
| **Orientador** | Diego Cirilo |

---

## 📄 Licença

Este projeto é desenvolvido para fins exclusivamente acadêmicos e educacionais, sob a licença [MIT](https://opensource.org/licenses/MIT).

---

Desenvolvido por **[Álvaro Yuri](https://github.com/alvarogit-ops)** 💈
