from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=30)
    sobrenome_cliente = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome_servico = models.CharField(max_length=80)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class Agendamento(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ManyToManyField(Servico)
    data_agendamento = models.DateField(auto_now_add=True)
    horario_agendamento = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['data_agendamento', 'horario_agendamento'], name='unico_agendamento'
            )
        ]