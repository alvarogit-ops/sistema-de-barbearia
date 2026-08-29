from django.db import models
# Create your models here.

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=30)
    sobrenome_cliente = models.CharField(max_length=30, blank=True)
    telefone = models.CharField(max_length=20, verbose_name='Telefone ou contato')

    class Meta:
        ordering = ['nome_cliente', 'sobrenome_cliente']

    def nome_completo(self):
        return f'{self.nome_cliente} {self.sobrenome_cliente}'.strip()

    def __str__(self):
        return self.nome_completo()

class Servico(models.Model):
    nome_servico = models.CharField(max_length=80)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome_servico

class Agendamento(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ManyToManyField(Servico) 
    data_agendamento = models.DateField()
    horario_agendamento = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['data_agendamento', 'horario_agendamento'], name='unico_agendamento'
            )
        ]

    def __str__(self):

        servicos = ' '.join(servico.nome_servico for servico in self.servico.all())
        # Como será mostrado no site, n tem nada haver com o que será mostrado no terminal
        return (f'ID:{self.id} Usuário: {self.usuario} Serviço: {servicos}, {self.data_agendamento}, {self.horario_agendamento}')
    