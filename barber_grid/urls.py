from django.urls import path
from . import views

#Define uma lista de url patterns

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name='login'), #aponta para uma função que existe em views. 
    path('registro', views.registro, name='registro'),
    path('painel_admin', views.painel_admin, name="painel_admin")
]

