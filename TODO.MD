## Início

1. Iniciar app
2. adicionar barber_grid.app.BarberGridConfig em settings.py
3. Criar urls.py dentro do app
4. Importar HttpResponse do django.http
5. retornar httpresponse com o nome do app
6. Criar url patterns dentro das 2 urls, no admin vai ter caminho para barber_grid urls

## Models

1. Criar model de agendamento
2. Impedir que clientes marquem no mesmo horário
3. Se cliente estiver vazio, ele será anônimo
4. Em seguida, relacionar com cliente, barbeiro e serviço
5. Rodar e aplicar as migrações
6. Testar criação de horários com conflito no terminal
