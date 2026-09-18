from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
#Define uma lista de url patterns

urlpatterns = [
    path('', views.setup, name="setup"),
    path('pagina_servicos', views.pagina_servicos, name="pagina_servicos"),
]

