from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#Define uma lista de url patterns

urlpatterns = [
    path('', views.setup, name="setup"),
    path('pagina_agendamento', views.pagina_agendamento, name="pagina_agendamento"),
    path('login/', views.login, name='login'), #aponta para uma função que existe em views. 
    path('registro', views.registro, name='registro'),
    path('painel_admin', views.painel_admin, name="painel_admin"),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:cliente_id>/excluir/', views.excluir_cliente, name='excluir_cliente'),
    path(
        'agendamentos/<int:agendamento_id>/status/',
        views.atualizar_status_agendamento,
        name='atualizar_status_agendamento',
    ),
    path('servicos/', views.servicos, name='servicos'),
    path('logout/', views.logoutForm, name='logout'),
    path('selecionar_data', views.selecionar_data, name='selecionar_data')
]

