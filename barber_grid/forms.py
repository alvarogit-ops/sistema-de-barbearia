from decimal import Decimal, InvalidOperation
from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Agendamento, Cliente, Servico

class RegisterForm(forms.ModelForm):
    usuario = forms.CharField(widget=forms.EmailInput)
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, label="Confirmar senha")

    class Meta:
        model = User
        fields = ['usuario', 'senha', 'confirmar_senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError("As senhas não combinam!")
        return cleaned_data


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico', 'data_agendamento', 'horario_agendamento']
        labels = {
            'servico': 'Serviço',
            'data_agendamento': 'Data',
            'horario_agendamento': 'Horário',
        }
        error_messages = {
            'servico': {
                'required': 'Selecione pelo menos um serviço.',
            },
            'data_agendamento': {
                'required': 'Informe a data do agendamento.',
                'invalid': 'Informe uma data válida.',
            },
            'horario_agendamento': {
                'required': 'Informe o horário do agendamento.',
                'invalid': 'Informe um horário válido.',
            },
        }
        widgets = {
            'servico': forms.CheckboxSelectMultiple(),
            'data_agendamento': forms.DateInput(attrs={
                'id': 'data_agendamento',
                'type': 'date',
            }),
            'horario_agendamento': forms.TimeInput(attrs={
                'id': 'horario_agendamento',
                'type': 'time',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servico'].queryset = Servico.objects.all()
        self.fields['servico'].help_text = ''

    def clean_data_agendamento(self):
        data = self.cleaned_data.get('data_agendamento')
        if data and data < timezone.localdate():
            raise forms.ValidationError('Escolha uma data a partir de hoje.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data_agendamento')
        horario = cleaned_data.get('horario_agendamento')
        if data and horario:
            agora = timezone.localtime()
            inicio = timezone.make_aware(datetime.combine(data, horario))
            if inicio <= agora:
                raise forms.ValidationError('Escolha um horário futuro.')
            conflito = Agendamento.objects.filter(
                data_agendamento=data,
                horario_agendamento=horario,
            )
            if self.instance.pk:
                conflito = conflito.exclude(pk=self.instance.pk)
            if conflito.exists():
                raise forms.ValidationError('Este horário já está ocupado. Escolha outro.')
        return cleaned_data


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_cliente', 'sobrenome_cliente', 'telefone']
        labels = {
            'nome_cliente': 'Nome',
            'sobrenome_cliente': 'Sobrenome',
            'telefone': 'Telefone ou contato',
        }
        error_messages = {
            'nome_cliente': {
                'required': 'Informe o nome do cliente.',
            },
            'telefone': {
                'required': 'Informe o telefone ou contato do cliente.',
            },
        }
        widgets = {
            'nome_cliente': forms.TextInput(attrs={
                'id': 'nome_cliente',
                'autocomplete': 'given-name',
            }),
            'sobrenome_cliente': forms.TextInput(attrs={
                'id': 'sobrenome_cliente',
                'autocomplete': 'family-name',
            }),
            'telefone': forms.TextInput(attrs={
                'id': 'telefone',
                'autocomplete': 'tel',
                'inputmode': 'tel',
            }),
        }

    def clean_nome_cliente(self):
        nome = (self.cleaned_data.get('nome_cliente') or '').strip()
        if not nome:
            raise forms.ValidationError('Informe o nome do cliente.')
        return nome

    def clean_sobrenome_cliente(self):
        return (self.cleaned_data.get('sobrenome_cliente') or '').strip()

    def clean_telefone(self):
        telefone = (self.cleaned_data.get('telefone') or '').strip()
        if not telefone:
            raise forms.ValidationError('Informe o telefone ou contato do cliente.')
        return telefone


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome_servico', 'preco', 'duracao_minutos']
        labels = {
            'nome_servico': 'Nome do serviço',
            'preco': 'Preço',
            'duracao_minutos': 'Duração estimada (minutos)',
        }
        error_messages = {
            'nome_servico': {
                'required': 'Informe o nome do serviço.',
            },
            'preco': {
                'required': 'Informe o preço do serviço.',
                'invalid': 'Informe um preço válido.',
            },
            'duracao_minutos': {
                'required': 'Informe a duração estimada do atendimento.',
                'invalid': 'Informe a duração em minutos, usando um número inteiro.',
            },
        }
        widgets = {
            'nome_servico': forms.TextInput(attrs={
                'id': 'nome_servico',
                'autocomplete': 'off',
            }),
            'preco': forms.NumberInput(attrs={
                'id': 'preco',
                'step': '0.01',
                'min': '0.01',
                'inputmode': 'decimal',
            }),
            'duracao_minutos': forms.NumberInput(attrs={
                'id': 'duracao_minutos',
                'min': '1',
                'step': '1',
                'inputmode': 'numeric',
            }),
        }

    def clean_nome_servico(self):
        nome = (self.cleaned_data.get('nome_servico') or '').strip()
        if not nome:
            raise forms.ValidationError('Informe o nome do serviço.')
        return nome

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is None:
            raise forms.ValidationError('Informe o preço do serviço.')
        try:
            preco = Decimal(preco)
        except (InvalidOperation, TypeError, ValueError):
            raise forms.ValidationError('Informe um preço válido.')
        if preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')
        return preco

    def clean_duracao_minutos(self):
        duracao = self.cleaned_data.get('duracao_minutos')
        if duracao is None:
            raise forms.ValidationError('Informe a duração estimada do atendimento.')
        if duracao < 1:
            raise forms.ValidationError('A duração deve ser de pelo menos 1 minuto.')
        return duracao