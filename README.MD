<div align="center">

# 💈 Barber Grid

**Uma experiência simples para consultar serviços e iniciar agendamentos em uma barbearia.**

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
[⚙️ Instalação](#️-como-executar-o-projeto) •
[📚 Documentação](#-documentação--links)

<br>

</div>

---

## 📋 Sobre o projeto

O **Barber Grid** é uma aplicação web acadêmica desenvolvida com Django para facilitar a consulta de serviços de uma barbearia e o início de um agendamento.

Na **Sprint 1**, o usuário poderá visualizar os serviços disponíveis, escolher um serviço e preencher um formulário simples com seus dados.

O projeto segue o padrão arquitetural **MVT (Model-View-Template)** do Django, com foco em uma implementação objetiva e na validação do fluxo principal da aplicação.

---

## 🎯 Objetivo da Sprint 1

Desenvolver um fluxo simples que permita ao usuário:

- Consultar os serviços disponíveis.
- Visualizar informações dos serviços.
- Escolher um serviço para agendamento.
- Preencher um formulário simples com seus dados.

> O escopo desta sprint está concentrado no fluxo de consulta e preenchimento do formulário, sem a implementação de um sistema completo de gestão de barbearia.

---

## 🚀 Funcionalidades

| Funcionalidade | Status |
|---|---|
| Consulta de serviços disponíveis | ✅ Concluído |
| Exibição de informações dos serviços | ✅ Concluído |
| Seleção de serviço | ✅ Concluído|


---

## 👥 Perfil de usuário

### 👤 Cliente

O cliente poderá consultar os serviços oferecidos pela barbearia, escolher um serviço e preencher um formulário simples para iniciar um agendamento.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Utilização |
|---|---|
| 🐍 Python | Linguagem do backend |
| 🟢 Django | Framework web |
| 🌐 HTML5 | Estrutura das páginas |
| 🎨 CSS3 | Estilização da interface |
| 🟨 JavaScript | Interações no frontend |
| 🟣 Bootstrap 5 | Componentes e responsividade |
| 🗃️ SQLite | Banco de dados |
| 🔧 Git & GitHub | Controle de versão |
| 🎨 Figma | Prototipação |

---

## 🏗️ Arquitetura (MVT)

O projeto utiliza o padrão **MVT (Model-View-Template)**, arquitetura padrão do Django.

| Componente | Responsabilidade |
|---|---|
| **Model** | Estrutura e persistência dos dados da aplicação. |
| **View** | Processamento das requisições e controle do fluxo. |
| **Template** | Renderização da interface visual para o usuário. |

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
├── config/             # Configurações do projeto Django
├── barber_grid/        # App principal
├── static/             # CSS, JavaScript e imagens
├── templates/          # Templates HTML
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git
├── manage.py           # Utilitário do Django
├── README.md           # Documentação principal
└── requirements.txt    # Dependências do projeto
```

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/alvarogit-ops/sistema-de-barbearia.git
cd barber-grid
```

### 2. Crie e ative o ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux ou macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`, caso necessário.

```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
```

### 5. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário

Execute o comando abaixo para criar um usuário administrador do Django:

```bash
python manage.py createsuperuser
```

Preencha as informações solicitadas:

* **Nome de usuário:** informe o nome de usuário do administrador.
* **E-mail:** informe o endereço de e-mail.
* **Senha:** crie uma senha segura e confirme-a.

> A senha não será exibida enquanto você digita no terminal.

### 7. Inicie o servidor

```bash
python manage.py runserver
```

Acesse a aplicação:

http://127.0.0.1:8000/

### 8. Cadastre um serviço pelo Django Admin

Após iniciar o servidor, acesse o painel administrativo:

http://127.0.0.1:8000/admin/

1. Faça login utilizando o nome de usuário e a senha do superusuário criado anteriormente.
2. Localize a seção **Serviços** no painel administrativo.
3. Clique em **Adicionar serviço**.
4. Preencha os dados do serviço:

   * **Nome do serviço:** nome do corte ou procedimento.
   * **Preço:** valor do serviço.
   * **Duração em minutos:** tempo estimado para realizar o serviço.
5. Salve o cadastro.

Após salvar, o serviço cadastrado estará disponível na página de serviços da aplicação.

---


## 🗃️ Modelos Principais

| Modelo | Descrição |
|---|---|
| **Serviço** | Representa os serviços oferecidos pela barbearia, conforme requisitos da Sprint 1. |


A estrutura dos modelos será definida de acordo com os critérios de aceitação e as necessidades do fluxo implementado.

---

## 📚 Documentação & Links

🔗 **[Protótipo no Figma](https://www.figma.com/design/DEjI9zGjpfAGLJwP4ejRe2/Barber-Scheduling---Prot%C3%B3tipo-de-Alta-Fidelidade?node-id=0-1&t=wsz3jwY1O719cKFE-1)**

📁 Documentação complementar e diagramas disponíveis na pasta `docs/`, na branch `docs`.

---

## 👨‍💻 Equipe

| Nome | Função |
|---|---|
| **Álvaro Yuri** | Project Owner, Scrum Master e Desenvolvedor |

🔗 [GitHub — alvarogit-ops](https://github.com/alvarogit-ops)

---

## ✅ Definition of Done (DoD)

Uma tarefa será considerada pronta quando:

- [ ] O código estiver na branch `main` por meio de um Pull Request revisado, conforme o fluxo definido para o projeto.
- [ ] A funcionalidade tiver sido testada manualmente.
- [ ] Todos os critérios de aceitação da Issue tiverem sido cumpridos.
- [ ] A Issue tiver sido fechada e movida para `Done`.

---

## 📌 Informações Acadêmicas

| Informação | Detalhes |
|---|---|
| **Instituição** | IFRN Campus São Paulo do Potengi |
| **Disciplina** | Projeto de Desenvolvimento de Sistemas para Internet |
| **Professora** | Fernanda Lígia |
| **Orientador** | Diego Cirilo |

---

## 📄 Licença

Desenvolvido para fins acadêmicos sob os termos da licença padrão de projetos educacionais.

<div align="center">

---

Desenvolvido por **[Álvaro Yuri](https://github.com/alvarogit-ops)** 💈

</div>
