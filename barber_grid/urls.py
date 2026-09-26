from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
#Define uma lista de url patterns

urlpatterns = [

    path('', views.setup, name="setup"),
    path('painel_admin', views.painel_admin, name="painel_admin"),
    path('login_view', views.login_view, name="login_view"),
    path('registro', views.registro, name="registro"),
    path('agendamento/<int:servico_id>/', views.agendamento, name='agendamento'),
    path('pagina_servicos', views.pagina_servicos, name="pagina_servicos"),
    path('historico_agendamentos', views.historico_agendamentos, name="historico_agendamentos"),
    path('servico', views.servico, name='servico')
]