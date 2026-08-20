from django.urls import path
from . import views

#Define uma lista de url patterns

urlpatterns = [
    path('', views.index)
]

