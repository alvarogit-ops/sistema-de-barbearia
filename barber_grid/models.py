from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cliente',
    )
    nome_cliente = models.CharField(max_length=30)
    sobrenome_cliente = models.CharField(max_length=30, blank=True)
    telefone = models.CharField(max_length=20, verbose_name='Telefone ou contato')

    class Meta:
        ordering = ['nome_cliente', 'sobrenome_cliente']

    def nome_completo(self):
        return f'{self.nome_cliente} {self.sobrenome_cliente}'.strip()

    def __str__(self):
        return self.nome_completo()

    @classmethod
    def para_usuario(cls, user):
        cliente = cls.objects.filter(user=user).first()
        if cliente:
            return cliente

        nome = (user.get_username() or '').strip()[:30] or 'Cliente'
        orfao = cls.objects.filter(user__isnull=True, nome_cliente=nome).first()
        if orfao:
            orfao.user = user
            orfao.save(update_fields=['user'])
            return orfao

        return cls.objects.create(
            user=user,
            nome_cliente=nome,
            telefone='Não informado',
        )

class Servico(models.Model):
    nome_servico = models.CharField(max_length=80)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    duracao_minutos = models.PositiveIntegerField(
        verbose_name='Duração estimada (minutos)',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ['nome_servico']

    def __str__(self):
        return self.nome_servico

class Agendamento(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'

    usuario = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ManyToManyField(Servico) 
    data_agendamento = models.DateField()
    horario_agendamento = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    class Meta:
        ordering = ['-data_agendamento', '-horario_agendamento']
        constraints = [
            models.UniqueConstraint(
                fields=['data_agendamento', 'horario_agendamento'], name='unico_agendamento'
            )
        ]

    def __str__(self):

        servicos = ' '.join(servico.nome_servico for servico in self.servico.all())
        # Como será mostrado no site, n tem nada haver com o que será mostrado no terminal
        return (f'ID:{self.id} Usuário: {self.usuario} Serviço: {servicos}, {self.data_agendamento}, {self.horario_agendamento}')
    