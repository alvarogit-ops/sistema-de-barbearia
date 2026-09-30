from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Servico(models.Model):
    nome_servico = models.CharField(max_length=80)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    duracao_minutos = models.PositiveIntegerField(
        verbose_name='Duração estimada (minutos)',
    )

    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)


    class Meta:
        ordering = ['nome_servico']

    def __str__(self):
        return self.nome_servico


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    telefone = models.CharField(max_length = 15)



class Agendamento(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )

    data = models.DateField()

    horario = models.TimeField()

    def __str__(self):
        return f"{self.cliente} - {self.servico} - {self.data} {self.horario}"