from django.db import models


class Servico(models.Model):
    """Tipos de serviço que a barbearia oferece, tipo cabelo, barba, sobrancelha"""
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    """Um agendamento para barbearia marcado pelo cliente"""
    cliente_nome = models.CharField(max_length=100)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    data_agendada = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente_nome} - {self.servico.nome}"

       
                                
                                
                                