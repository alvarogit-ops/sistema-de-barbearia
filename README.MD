# 💈 Barber Grid

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=092E20)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white&labelColor=7952B3)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black&labelColor=F7DF1E)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=003B57)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-750014?style=for-the-badge&labelColor=750014)](https://opensource.org/licenses/MIT)

Sistema web para gestão de estabelecimentos de estética masculina, desenvolvido com o objetivo de auxiliar na organização de informações e processos relacionados à rotina de uma barbearia.

O **Barber Grid** encontra-se em desenvolvimento acadêmico e busca centralizar funcionalidades administrativas de acordo com as necessidades identificadas durante o levantamento de requisitos do estabelecimento.

---

## 📋 Sobre o Projeto

O **Barber Grid** é um sistema de gestão acadêmico voltado para a organização das rotinas operacionais de barbearias.

A aplicação está sendo desenvolvida com **Django** e segue o padrão arquitetural **MVT (Model-View-Template)**. Os requisitos e funcionalidades do sistema são definidos e refinados a partir do levantamento das necessidades do estabelecimento.

| Atributo | Detalhes |
|---|---|
| **Linguagem** | Python 3.10+ |
| **Framework** | Django 6.1 |
| **Arquitetura** | MVT (Model-View-Template) |
| **Banco de Dados** | SQLite (desenvolvimento) |
| **Front-end** | HTML5, CSS3, JavaScript e Bootstrap 5 |
| **Controle de Versão** | Git e GitHub |
| **Prototipação** | Figma |

---

## 🎯 Contexto do Projeto

O gerenciamento das atividades de uma barbearia envolve diferentes processos, como organização dos profissionais, serviços oferecidos, clientes, atendimentos e horários.

O **Barber Grid** está sendo desenvolvido com o propósito de investigar e atender às necessidades identificadas no funcionamento real do estabelecimento.

O levantamento e a validação dos requisitos são utilizados para definir quais problemas devem ser solucionados pelo sistema e quais funcionalidades são relevantes para a operação da barbearia.

Entre os aspectos considerados inicialmente estão:

- Organização das informações do estabelecimento;
- Gerenciamento dos profissionais;
- Organização dos serviços oferecidos;
- Cadastro e gerenciamento de clientes;
- Controle e acompanhamento dos atendimentos;
- Organização de horários e agendamentos;
- Controle do status dos atendimentos;
- Centralização das informações operacionais.

---

## 🚀 Funcionalidades

As funcionalidades do sistema encontram-se em desenvolvimento e são refinadas conforme o levantamento e a validação dos requisitos.

| Funcionalidade | Status |
|---|---|
| Autenticação de usuários | 🚧 Em desenvolvimento |
| Área restrita de gerenciamento | 🚧 Em desenvolvimento |
| Gerenciamento de serviços | 🚧 Em desenvolvimento |
| Gerenciamento de profissionais | 🚧 Em desenvolvimento |
| Organização dos atendimentos | 🔎 Em validação |
| Sistema de agendamentos | 🔎 Em validação |
| Cadastro e gerenciamento de clientes | 🔎 Em validação |
| Controle de status dos atendimentos/agendamentos | 🔎 Em validação |
| Prevenção de conflitos de horários | 🔎 Em validação |

> **Observação:** As funcionalidades marcadas como **Em validação** poderão ser modificadas, substituídas ou removidas conforme os resultados do levantamento de requisitos.

---

## 👥 Usuários do Sistema

Os perfis e níveis de acesso do **Barber Grid** estão sendo definidos e refinados de acordo com as necessidades identificadas no estabelecimento.

Inicialmente, o sistema possui uma área destinada à utilização pelos responsáveis e profissionais da barbearia.

A necessidade de acesso direto por clientes, bem como possíveis formas de interação externa com o sistema, será definida após a validação dos requisitos e da rotina real do estabelecimento.

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|---|---|
| **Linguagem de Back-end** | Python |
| **Framework Web** | Django |
| **Linguagem Front-end** | JavaScript |
| **Estruturação** | HTML5 |
| **Estilização** | CSS3 e Bootstrap 5 |
| **Banco de Dados** | SQLite |
| **Controle de Versão** | Git e GitHub |
| **Prototipação** | Figma |

---

## 🏗️ Arquitetura — MVT

A aplicação utiliza o padrão arquitetural **MVT (Model-View-Template)** fornecido pelo Django.

| Componente | Responsabilidade |
|---|---|
| **Model** | Representação e organização dos dados da aplicação, além das regras relacionadas à persistência e aos relacionamentos entre entidades. |
| **View** | Processamento das requisições HTTP, execução da lógica da aplicação e comunicação entre Models e Templates. |
| **Template** | Apresentação da interface visual para o usuário utilizando HTML, Bootstrap e JavaScript. |

---

## 🗃️ Modelagem Inicial

A modelagem de dados do **Barber Grid** encontra-se em evolução e será refinada conforme o levantamento e a validação dos requisitos do estabelecimento.

Entre as entidades inicialmente consideradas estão:

| Entidade | Possível Responsabilidade |
|---|---|
| **Profissional / Barbeiro** | Representar os profissionais responsáveis pelos atendimentos. |
| **Serviço** | Representar os serviços oferecidos pelo estabelecimento. |
| **Cliente** | Armazenar informações cadastrais e de contato dos clientes. |
| **Atendimento** | Representar informações relacionadas ao fluxo de atendimento da barbearia. |
| **Agendamento** | Representar a organização de horários, relacionando cliente, profissional, serviço, data, horário e status. |

A estrutura definitiva das entidades e seus relacionamentos será definida e refinada conforme a evolução do levantamento de requisitos.

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
├── config/                 # Configurações do projeto Django
│
├── barber_grid/            # Aplicação principal
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ...
│
├── static/                 # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/              # Templates HTML
│
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── manage.py               # Utilitário de linha de comando do Django
├── README.md               # Documentação principal
└── requirements.txt        # Dependências do projeto
```


## ⚙️ Como Executar o Projeto

1. Clone o repositório

git clone https://github.com/alvarogit-ops/sistema-de-barbearia.git
cd barber-grid

«Nota: Certifique-se de que o nome da pasta criada pelo clone corresponde a "barber-grid". Caso contrário, utilize o nome correto da pasta ao executar o comando "cd".»

2. Crie e ative o ambiente virtual

Windows

python -m venv venv
venv\Scripts\activate

Linux ou macOS

python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Configure as variáveis de ambiente

Crie um arquivo ".env" na raiz do projeto com base no arquivo ".env.example".

Exemplo:

SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True

«Importante: Em ambientes de produção, utilize uma "SECRET_KEY" segura e mantenha "DEBUG=False".»

5. Execute as migrações

Aplique as migrações do banco de dados:

python manage.py makemigrations
python manage.py migrate

6. Inicie o servidor

Execute o servidor de desenvolvimento:

python manage.py runserver

Acesse o sistema pelo endereço:

http://127.0.0.1:8000/

---

🗃️ Modelos Principais

Os principais modelos considerados inicialmente no sistema são:

Modelo| Descrição
Cliente| Armazena dados cadastrais e de contato dos clientes.
Barbeiro| Representa os profissionais prestadores de serviços.
Serviço| Define os procedimentos oferecidos, como corte e barba, além de seus respectivos preços.
Agendamento| Relaciona cliente, barbeiro, serviço, data, horário e status do agendamento.

«A estrutura dos modelos poderá ser alterada conforme a evolução do levantamento e da validação dos requisitos.»

---

📚 Documentação e Links

- 🔗 "Protótipo no Figma" (https://www.figma.com/design/wg6zSJiM4ZmavHRpLdMBUp/Barber-Grid---Alta-Fidelidade?node-id=0-1&p=f&t=QkXnF0ZuE4NUrFYx-0)
- 📁 Documentação complementar e diagramas estão disponíveis, ou serão disponibilizados, na pasta "docs/".

---

👨‍💻 Equipe

Nome| Função
Álvaro Yuri| Project Owner, Scrum Master e Desenvolvedor

---

📌 Informações Acadêmicas

- Instituição: IFRN
- Disciplina: Projeto de Desenvolvimento de Sistemas para Internet
- Professora: Fernanda Lígia
- Orientador: Diego Cirilo

---

📄 Licença

Este projeto é desenvolvido para fins acadêmicos e está disponibilizado sob os termos da Licença MIT.

Consulte o arquivo "LICENSE" para obter os termos completos da licença.