from django.db import models


# Create your models here.



class Servico(models.Model):
    servico = models.CharField(max_length=80)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    duracao_minutos = models.PositiveIntegerField(
        verbose_name='Duração estimada (minutos)',
    )

    class Meta:
        ordering = ['servico']

    def __str__(self):
        return self.servico

