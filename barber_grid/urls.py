from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
#Define uma lista de url patterns

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('painel_admin', views.painel_admin, name="painel_admin"),
    path('login', views.login, name="login"),
    path('registro', views.registro, name="registro"),

    path('agendamento/<int:servico_id>/', views.agendamento, name='agendamento'),

    path('pagina_servicos', views.pagina_servicos, name="pagina_servicos"),
    path('historico_agendamentos', views.historico_agendamentos, name="historico_agendamentos"),
    path('servico', views.servico, name='servico'),
    path('usuario_historico', views.usuario_historico, name='usuario_historico'),

    path(
        "horarios-disponiveis/",
        views.horarios_disponiveis,
        name="horarios_disponiveis"
    ),

    path(
        "confirmar-agendamento/<int:servico_id>",
        views.confirmar_agendamento,
        name="confirmar_agendamento"
    ),

    path(
        'enviado/<int:agendamento_id>/',
        views.enviado,
        name='enviado'
    ),

    path(
        "detalhe-agendamento/<int:agendamento_id>/",
        views.detalhe_agendamento,
        name="detalhe_agendamento"
    ),
    path(
    "cancelar-agendamento/<int:agendamento_id>/",
    views.cancelar_agendamento,
    name="cancelar_agendamento"
),
path(
    "editar-perfil/",
    views.editar_perfil,
    name="editar_perfil"
),
]