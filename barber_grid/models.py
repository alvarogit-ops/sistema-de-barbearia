<<<<<<< HEAD
from django.db import models
=======
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone



# Create your models here.



class Servico(models.Model):
    nome_servico = models.CharField(max_length=80)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
<<<<<<< HEAD
    )
    duracao_minutos = models.PositiveIntegerField(
        verbose_name='Duração estimada (minutos)',
    )

    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)


    class Meta:
        ordering = ['nome_servico']

    def __str__(self):
        return self.nome_servico

class Agendamento(models.Model):
    cliente = models.CharField(max_length=100)
