from django import forms
from .models import Agendamento


class ClientesForm(forms.ModelForm): #de onde vem forms.ModelForm
    class Meta: #por que cria classe meta?
        model = Agendamento
        fields = ['barbeiro', 'cliente_nome_balcao', 'servico', 'data_agendada']
        labels = {'barbeiro': 'Escolhe o Barbeiro',
                  'cliente_nome_balcao': 'Nome do Cliente (Balcão)',
                  'serviço': 'Serviço',
                  'data_agendada': 'Data e Horário'} #por que usar label?

    
    