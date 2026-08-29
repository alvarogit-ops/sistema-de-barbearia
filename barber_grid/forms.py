from django import forms
from django.contrib.auth.models import User

from .models import Cliente

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
class AgendamentoForm(forms.Form):
    pass


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