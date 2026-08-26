from django import forms
from django.contrib.auth.models import User

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