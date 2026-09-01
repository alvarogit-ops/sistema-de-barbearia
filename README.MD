# 💈 Barber Grid

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=092E20)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white&labelColor=7952B3)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black&labelColor=F7DF1E)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=003B57)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-750014?style=for-the-badge&labelColor=750014)](https://opensource.org/licenses/MIT)


Sistema web para gestão de estabelecimentos de estética masculina, desenvolvido com o objetivo de auxiliar no gerenciamento de clientes, serviços e agendamentos. O **Barber Grid** facilita a organização da barbearia, permitindo o controle de informações vitais e a redução de conflitos de horários.

---

## 📋 Sobre o projeto

O **Barber Grid** é um sistema de gestão acadêmico projetado para otimizar rotinas de barbearias. A arquitetura da aplicação é baseada no framework **Django**, utilizando o padrão **MVT (Model-View-Template)**.

| Atributo | Detalhes do Projeto |
| :--- | :--- |
| **Framework** | Django (Python) |
| **Arquitetura** | MVT (Model-View-Template) |
| **Banco de Dados** | SQLite (Desenvolvimento) |
| **Front-end** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **Controle de Versão** | Git & GitHub |

---

## 🎯 Problema & Solução

| Desafios do Gerenciamento Manual | Soluções Propostas pelo Barber Grid |
| :--- | :--- |
| Conflitos frequentes entre horários | Sistema automatizado de checagem de disponibilidade |
| Dificuldade no controle de clientes | Centralização de cadastros e histórico |
| Desorganização dos serviços ofertados | Catálogo estruturado de procedimentos e durações |
| Falta de centralização de dados | Plataforma web unificada para equipe e gestores |

---

## 🚀 Funcionalidades

| Funcionalidade | Status |
| :--- | :---: |
| Cadastro de clientes |  Em desenvolvimento |
| Cadastro de serviços |  Em desenvolvimento |
| Cadastro de barbeiros |  Em desenvolvimento |
| Sistema de agendamentos |  Em desenvolvimento |
| Controle de status de agendamentos |  Em desenvolvimento |
| Autenticação de usuários | Em desenvolvimento |
| Área restrita de gerenciamento | Em desenvolvimento |
| Prevenção de conflitos de horários | Em desenvolvimento |

---

## 👥 Perfis de Usuários

* **Cliente:** Visualiza serviços disponíveis e realiza agendamentos online.
* **Barbeiro / Administrador:** Gerencia o fluxo de atendimento, clientes, serviços e horários da barbearia.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem Backend:** Python
* **Framework Web:** Django
* **Linguagem Frontend:** JavaScript
* **Estilização:** CSS, Bootstrap
* **Banco de Dados:** SQLite
* **Ferramentas:** Git, GitHub, Figma

---

## 🏗️ Arquitetura (MVT)

* **Model:** Responsável pela estrutura de dados e regras de negócio com o ORM do Django.
* **View:** Processa as requisições HTTP, executa a lógica e interage com os Models.
* **Template:** Renderiza a interface visual para o usuário utilizando HTML, Bootstrap e scripts em JavaScript.

---

## 📁 Estrutura do Projeto

```text
barber-grid/
│
├── .github/
│   └── ISSUE_TEMPLATE/
│
├── docs/
│   ├── README.md
│   ├── diagramas/
│   └── prototipos/
│
├── config/             # Configurações do projeto Django (settings, urls, etc.)
├── barber_grid/        # App principal (models, views, forms, migrations)
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── templates/          # Arquivos HTML globais e específicos
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git
├── manage.py           # Utilitário de linha de comando do Django
├── README.md           # Documentação principal
└── requirements.txt    # Dependências do projeto
```
## ⚙️ Como Executar o Projeto


### 1. Clone o repositório

```bash
git clone https://github.com/alvarogit-ops/barber-management-system-grid.git
cd barber-grid
```

### 2. Crie e ative o ambiente virtual

**No Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux ou macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`:

```plaintext
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
```

### 5. Execute as migrações e inicie o servidor

Execute as migrações do banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate
```

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse o sistema em:

`http://127.0.0.1:8000/`

---

## 🗃️ Modelos Principais

| Modelo | Descrição |
| :--- | :--- |
| **Cliente** | Armazena dados cadastrais e de contato dos clientes. |
| **Barbeiro** | Cadastra os profissionais prestadores de serviço. |
| **Serviço** | Define os procedimentos ofertados (ex: Corte, Barba) e preços. |
| **Agendamento** | Relaciona cliente, barbeiro, serviço, data, hora e status. |

---

## 📚 Documentação & Links

* 🔗 **[Protótipo no Figma](https://www.figma.com/design/wg6zSJiM4ZmavHRpLdMBUp/Barber-Grid---Alta-Fidelidade?node-id=0-1&p=f&t=QkXnF0ZuE4NUrFYx-0)**
* Documentação complementar e diagramas disponíveis na pasta `docs/`.

---

## 👨‍💻 Equipe

| Nome | Função |
| :--- | :--- |
| **Álvaro Yuri** | Project Owner, Scrum Master, Desenvolvedor |

---

## 📌 Informações Acadêmicas

* **Instituição:** IFRN 
* **Disciplina:** Projeto de Desenvolvimento de Sistemas para Internet
* **Professora:** Fernanda Lígia
* **Orientador:** Diego Cirilo

---

## 📄 Licença

Desenvolvido para fins acadêmicos sob os termos da licença padrão de projetos educacionais.
