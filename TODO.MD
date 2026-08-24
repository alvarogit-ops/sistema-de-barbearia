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