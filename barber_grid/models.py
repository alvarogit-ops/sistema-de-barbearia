from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

DIA_DA_SEMANA_CHOICES = [
    (0, 'Segunda-Feira'),
    (1, 'Terça-Feira'),
    (2, 'Quarta-Feira'),
    (3, 'Quinta-Feira'),
    (4, 'Sexta-Feira'),
    (5, 'Sábado'),
    (6, 'Domingo'),
]

# Feriados nacionais de data fixa: (mês, dia). Fonte única (o JS não tem mais lista).
DIAS_FERIADO = [
    (1, 1),    # Confraternização Universal
    (4, 21),   # Tiradentes
    (5, 1),    # Dia do Trabalho
    (9, 7),    # Independência do Brasil
    (10, 12),  # Nossa Senhora Aparecida
    (11, 2),   # Finados
    (11, 15),  # Proclamação da República
    (11, 20),  # Dia Nacional de Zumbi e da Consciência Negra
    (12, 25),  # Natal
]


class Servico(models.Model):
    nome_servico = models.CharField(max_length=80)

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    duracao_minutos = models.PositiveIntegerField(
        verbose_name='Duração estimada (minutos)',
    )

    imagem = models.ImageField(
        upload_to='servicos/',
        blank=True,
        null=True,
    )

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome_servico']

    def __str__(self):
        return self.nome_servico


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class HorariodeFuncionamento(models.Model):
    dia_inicio = models.PositiveSmallIntegerField(choices=DIA_DA_SEMANA_CHOICES)
    dia_fim = models.PositiveSmallIntegerField(choices=DIA_DA_SEMANA_CHOICES)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def clean(self):
        if self.horario_inicio and self.horario_fim:
            if self.horario_inicio >= self.horario_fim:
                raise ValidationError(
                    'O horário de início deve ser anterior ao horário de fim.'
                )

        if self.dia_inicio is not None and self.dia_fim is not None:
            if self.dia_inicio > self.dia_fim:
                raise ValidationError(
                    'O dia de início não pode ser depois do dia de fim.'
                )

    def __str__(self):
        return (
            f'{self.get_dia_inicio_display()} a {self.get_dia_fim_display()}, '
            f'{self.horario_inicio:%H:%M}–{self.horario_fim:%H:%M}'
        )


class BloqueioHorario(models.Model):
    data_inicio = models.DateField()
    data_fim = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    motivo = models.CharField(max_length=50)

    def clean(self):
        if self.data_inicio and self.data_fim:
            if self.data_inicio > self.data_fim:
                raise ValidationError(
                    'A data de início não pode ser depois da data de fim.'
                )

        if self.horario_inicio and self.horario_fim:
            if self.horario_inicio >= self.horario_fim:
                raise ValidationError(
                    'O horário de início deve ser anterior ao horário de fim.'
                )

    def __str__(self):
        return (
            f'{self.motivo}: {self.data_inicio:%d/%m/%Y} a '
            f'{self.data_fim:%d/%m/%Y}, '
            f'{self.horario_inicio:%H:%M}–{self.horario_fim:%H:%M}'
        )


class Agendamento(models.Model):
    class Status(models.TextChoices):
        SOLICITADO = 'solicitado', 'Solicitado'
        CONFIRMADO = 'confirmado', 'Confirmado'
        CANCELADO = 'cancelado', 'Cancelado'

    # PROTECT: apagar um cliente/serviço não apaga o histórico.
    # Para retirar um serviço do ar, use ativo=False.
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
    )

    barbeiro = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='agendamentos_como_barbeiro',
    )

    data = models.DateField()

    horario = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SOLICITADO,
    )

    observacoes = models.CharField(max_length=500, blank=True)

    criado_em = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['data', 'horario'],
                condition=~models.Q(status='cancelado'),
                name='unico_agendamento_ativo',
            )
        ]

    def __str__(self):
        return f'{self.cliente} - {self.servico} - {self.data} {self.horario}'