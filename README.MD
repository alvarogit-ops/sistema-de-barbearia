<div align="center">

# 💈 Barber Grid

**Uma experiência simples e intuitiva para consultar serviços e agendar horários em uma barbearia.**

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
[⚙️ Como Executar](#️-como-executar-o-projeto) •
[📚 Documentação](#-documentação--links)

<br>

</div>

---

## 📋 Sobre o projeto

O **Barber Grid** é uma aplicação web desenvolvida com Django para gestão de agendamentos em barbearias. A plataforma conecta clientes e administradores/barbeiros em uma interface simples e moderna, permitindo a navegação por serviços, escolha de datas/horários disponíveis e acompanhamento dos agendamentos em tempo real.

O projeto foi construído seguindo o padrão arquitetural **MVT (Model-View-Template)** nativo do Django, garantindo separação clara de responsabilidades, facilidade de manutenção e validações sólidas no backend.

---

## 🚀 Funcionalidades

### 👤 Área do Cliente
- **Autenticação de Usuário:** Registro e login seguros com perfil de cliente integrado.
- **Catálogo de Serviços:** Visualização de cortes e procedimentos com fotos, descrições, preços e tempo estimado de duração.
- **Consulta de Horários Disponíveis:** Verificação automatizada de horários livres considerando os horários de funcionamento da barbearia e bloqueios cadastrados.
- **Agendamento Completo:** Seleção de serviço, data e horário com confirmação e validação de conflitos de agenda.
- **Painel do Cliente:** Acompanhamento da próxima reserva e histórico detalhado dos agendamentos (Solicitado, Confirmado, Cancelado).
- **Cancelamento:** Possibilidade de cancelar agendamentos ativos diretamente pelo painel.

### 💈 Área Administrativa / Barbeiro
- **Painel de Gestão (Admin Dashboard):** Visualização cronológica dos agendamentos realizados.
- **Gerenciamento de Serviços:** Cadastro, atualização e remoção de serviços oferecidos.
- **Controle de Status:** Confirmação ou cancelamento de agendamentos solicitados.
- **Configuração de Horários & Bloqueios:** Cadastro de horários de funcionamento e bloqueios de agenda por intervalo de datas/horas.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função / Utilização |
|---|---|
| 🐍 **Python 3.10+** | Linguagem principal do backend |
| 🟢 **Django 6.1** | Framework web (rotas, ORM, autenticação, MVT) |
| 🖼️ **Pillow** | Processamento e upload de imagens dos serviços |
| 🌐 **HTML5 / CSS3** | Estrutura semântica e estilização customizada |
| 🟣 **Bootstrap 5** | Componentes visuais responsivos e layout grid |
| 🟨 **JavaScript (ES6+)** | Interações assíncronas (fetch de horários) e dinamismo na interface |
| 🗃️ **SQLite** | Banco de dados relacional para ambiente de desenvolvimento |
| 🔧 **Git & GitHub** | Controle de versão e colaboração |

---

## 🏗️ Arquitetura (MVT)

O projeto utiliza o padrão **MVT (Model-View-Template)** do Django:

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
┌──────────────────────────────┐       ┌──────────────────────────────┐
│       Models (models.py)     │       │    Templates (HTML/CSS/JS)   │
│ (Servico, Agendamento, etc.) │       │  (inicio.html, login.html)   │
└──────────────────────────────┘       └──────────────────────────────┘

```

---

## 🗃️ Modelos Principais

* **`Servico`**: Guarda informações como `nome_servico`, `preco`, `duracao_minutos` e `imagem`.
* **`Cliente`**: Vinculado ao model `User` nativo do Django para adicionar o campo `telefone`.
* **`HorariodeFuncionamento`**: Define os dias da semana (`dia_inicio`, `dia_fim`) e faixas de horários atendidos.
* **`BloqueioHorario`**: Define intervalos de datas e horas bloqueadas para novos agendamentos.
* **`Agendamento`**: Conecta `Cliente` e `Servico` a uma `data` e `horario`, controlando o `status` (`solicitado`, `confirmado`, `cancelado`) e garantindo unicidade de horário ativo via constraint no banco.

---

## 📁 Estrutura do Projeto

```text
barber-grid/
│
├── .github/                 # Templates de issues e workflows do GitHub
├── docs/                    # Documentação complementar, protótipos e diagramas
├── config/                  # Configurações globais do projeto Django (settings.py, urls.py)
├── barber_grid/             # App principal da aplicação
│   ├── admin.py             # Registro de models no Django Admin
│   ├── apps.py              # Configuração do app barber_grid
│   ├── models.py            # Definição dos modelos de dados (Servico, Agendamento, etc.)
│   ├── tests.py             # Suíte de testes automatizados (unitários e integração)
│   ├── urls.py              # Mapeamento das rotas do app
│   └── views.py             # Lógica de negócios e manipuladores de requisição
├── static/                  # Arquivos estáticos (CSS, JavaScript, Imagens)
├── templates/               # Arquivos HTML renderizados pelo Django
│   └── barber_grid/
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore               # Regras de ignorados pelo Git
├── manage.py                # Utilitário de linha de comando do Django
├── README.md                # Documentação principal do repositório
└── requirements.txt         # Dependências do projeto Python

```

---

## ⚙️ Como Executar o Projeto

### Pró-requisitos

* **Python 3.10+** instalado
* **Git** instalado

### 1. Clonar o repositório

```bash
git clone [https://github.com/alvarogit-ops/sistema-de-barbearia.git](https://github.com/alvarogit-ops/sistema-de-barbearia.git)
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

### 3. Instalar dependências

Com o ambiente virtual ativado, instale os pacotes listados no `requirements.txt`:

```bash
pip install -r requirements.txt

```

*(Caso utilize o comando direto: `pip install django pillow`)*

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto copiando as definições do `.env.example`:

```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True

```

### 5. Executar as migrações do banco de dados

```bash
python manage.py makemigrations
python manage.py migrate

```

### 6. Criar um superusuário (Administrador / Barbeiro)

Para acessar o painel administrativo do Django e cadastrar serviços iniciais:

```bash
python manage.py createsuperuser

```

Preencha o nome de usuário, e-mail e senha conforme as solicitações no terminal.

### 7. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver

```

Acesse no navegador: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Como Executar os Testes Automatizados

O projeto possui uma suíte de testes cobrindo formulários, autenticação, controle de permissões e integridade das regras de agendamento. Para executá-los:

```bash
python manage.py test barber_grid

```

---

## 📚 Documentação & Links

* 🎨 **[Protótipo no Figma](https://www.figma.com/design/DEjI9zGjpfAGLJwP4ejRe2/Barber-Scheduling---Prot%C3%B3tipo-de-Alta-Fidelidade?node-id=0-1&t=wsz3jwY1O719cKFE-1)**
* 📁 Diagramas e documentação das Sprints disponíveis no diretório [`docs/`](https://www.google.com/search?q=./docs/).

---

## 👥 Equipe & Desenvolvimento

| Nome | Função | GitHub |
| --- | --- | --- |
| **Álvaro Yuri** | Project Owner, Scrum Master e Desenvolvedor Full-Stack | [@alvarogit-ops](https://github.com/alvarogit-ops) |

---

## 📌 Informações Acadêmicas

| Campo | Detalhes |
| --- | --- |
| **Instituição** | Instituto Federal do Rio Grande do Norte (IFRN) — Campus São Paulo do Potengi |
| **Curso** | Tecnologia em Sistemas para Internet |
| **Disciplina** | Projeto de Desenvolvimento de Sistemas para Internet |
| **Professora** | Fernanda Lígia |
| **Orientador** | Diego Cirilo |

---

## 📄 Licença

Este projeto é desenvolvido para fins exclusivamente acadêmicos e educacionais sob a licença [MIT](https://opensource.org/licenses/MIT).

---

Desenvolvido por **[Álvaro Yuri](https://github.com/alvarogit-ops)** 💈
