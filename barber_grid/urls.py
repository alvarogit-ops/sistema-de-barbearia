from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agendamento', views.agendamento, name="agendamento"),
    path('agendamento<cliente_id>/', views.agendamento, name='agendamento') #como vou adicionar o cliente_id aqui? #vou precisar de uma view nova para isso? 
]
