from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agendamento', views.agendamento, name="agendamento"),
    path('agendamentos<int:cliente_id>/', views.agendamento, name='agendamento_cliente'), #como vou adicionar o cliente_id aqui? #vou precisar de uma view nova para isso? Até adicionei int
    path('cadastro_clientes', views.cadastro_clientes, name='cadastro_clientes'), #como garanto que crio views.cadastro_clientes

]
