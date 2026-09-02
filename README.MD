# 💈 Barber Grid

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=092E20)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white&labelColor=7952B3)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black&labelColor=F7DF1E)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=003B57)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-750014?style=for-the-badge&labelColor=750014)](https://opensource.org/licenses/MIT)



Sistema web para gestão de estabelecimentos de estética masculina, desenvolvido com o objetivo de auxiliar na organização de informações e processos relacionados à rotina da barbearia.
O Barber Grid encontra-se em desenvolvimento acadêmico e busca centralizar funcionalidades administrativas de acordo com as necessidades identificadas no levantamento de requisitos do estabelecimento.

## 📋 Sobre o projeto

O Barber Grid é um sistema de gestão acadêmico voltado para a organização das rotinas operacionais de barbearias.
A aplicação está sendo desenvolvida com Django e segue o padrão arquitetural MVT (Model-View-Template). Os requisitos e funcionalidades do sistema são definidos e refinados a partir do levantamento das necessidades do estabelecimento.
| Atributo | Detalhes do Projeto |
|---|---|
| Framework | Django (Python) |
| Arquitetura | MVT (Model-View-Template) |
| Banco de Dados | SQLite (Desenvolvimento) |
| Front-end | HTML5, CSS3, JavaScript e Bootstrap 5 |
| Controle de Versão | Git e GitHub |

##🎯 Contexto do Projeto

O gerenciamento das atividades de uma barbearia pode envolver diferentes processos, como organização dos profissionais, serviços oferecidos, atendimentos e outras informações operacionais.
O Barber Grid está sendo desenvolvido para investigar e atender necessidades identificadas no funcionamento real do estabelecimento.
O levantamento e a validação dos requisitos são utilizados para definir quais problemas devem ser solucionados pelo sistema e quais funcionalidades fazem sentido para a operação da barbearia.
Entre os aspectos considerados inicialmente estão:
•
Organização das informações do estabelecimento;
•
Gerenciamento dos profissionais;
•
Organização dos serviços oferecidos;
•
Controle e acompanhamento dos atendimentos;
•
Possível organização de horários, conforme a necessidade identificada;
•
Centralização de informações operacionais.

## 🚀 Funcionalidades

As funcionalidades do sistema encontram-se em desenvolvimento e refinamento conforme o levantamento de requisitos.
| Funcionalidade | Status |
|---|---|
| Autenticação de usuários | Em desenvolvimento |
| Área restrita de gerenciamento | Em desenvolvimento |
| Gerenciamento de serviços | Em desenvolvimento |
| Gerenciamento de profissionais | Em desenvolvimento |
| Organização dos atendimentos | Em validação |
| Sistema de agendamentos | Em validação |
| Cadastro e gerenciamento de clientes | Em validação |
| Controle de status dos atendimentos/agendamentos | Em validação |
| Prevenção de conflitos de horários | Em validação |
As funcionalidades marcadas como Em validação poderão ser modificadas, substituídas ou removidas conforme os resultados do levantamento de requisitos.

## 👥 Usuários do Sistema

Os perfis e níveis de acesso do Barber Grid estão sendo definidos e refinados de acordo com as necessidades identificadas no estabelecimento.
Inicialmente, o sistema possui uma área destinada à utilização pelos responsáveis e profissionais da barbearia.
A necessidade de acesso direto por clientes, bem como possíveis formas de interação externa com o sistema, será definida após a validação dos requisitos e da rotina real do estabelecimento.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|---|---|
| Linguagem Backend | Python |
| Framework Web | Django |
| Linguagem Front-end | JavaScript |
| Estruturação | HTML5 |
| Estilização | CSS3 e Bootstrap 5 |
| Banco de Dados | SQLite |
| Controle de Versão | Git e GitHub |
| Prototipação | Figma |

## 🏗️ Arquitetura — MVT

A aplicação utiliza o padrão arquitetural MVT (Model-View-Template) do Django.
| Componente | Responsabilidade |
|---|---|
| Model | Representação e organização dos dados da aplicação, além das regras relacionadas à persistência e aos relacionamentos entre entidades. |
| View | Processamento das requisições HTTP, execução da lógica da aplicação e comunicação entre Models e Templates. |
| Template | Apresentação da interface visual para o usuário utilizando HTML, Bootstrap e scripts em JavaScript. |
🗃️ Modelagem Inicial
A modelagem de dados do Barber Grid encontra-se em evolução e será refinada conforme o levantamento e a validação dos requisitos do estabelecimento.
Entre as entidades inicialmente consideradas estão:
| Entidade | Possível Responsabilidade |
|---|---|
| Profissional / Barbeiro | Representar os profissionais responsáveis pelos atendimentos. |
| Serviço | Representar os serviços oferecidos pelo estabelecimento. |
| Cliente | Entidade em validação, cuja necessidade e responsabilidade serão definidas conforme os requisitos identificados. |
| Atendimento | Representar informações relacionadas ao fluxo de atendimento da barbearia. |
| Agendamento | Entidade em validação, cuja necessidade dependerá da forma como o estabelecimento organiza seus horários e atendimentos. |
A estrutura definitiva das entidades e seus relacionamentos será definida e refinada conforme a evolução do levantamento de requisitos.

## 📁 Estrutura do Projeto
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
│
├── barber_grid/        # Aplicação principal
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── migrations/
│   └── ...
│
├── static/             # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/          # Templates HTML
│
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git
├── manage.py           # Utilitário de linha de comando do Django
├── README.md           # Documentação principal
└── requirements.txt    # Dependências do projeto


## ⚙️ Como Executar o Projeto


### 1. Clone o repositório

```bash
git clone https://github.com/alvarogit-ops/sistema-de-barbearia.git
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
* Documentação complementar e diagramas ainda vão estar disponíveis na pasta `docs/`.

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
